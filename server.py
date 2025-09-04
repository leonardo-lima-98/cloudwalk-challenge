# server.py

from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime
import pandas as pd
from model import rolling_alert_recommendation

DB_PATH = "monitor.db"
app = FastAPI(title="Incident Monitor API")

class TxnEvent(BaseModel):
    ts: datetime
    status: str
    count: int = 1

@app.on_event("startup")
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        ts TEXT NOT NULL,
        status TEXT NOT NULL,
        count INTEGER NOT NULL
    )
    """)
    conn.commit()
    conn.close()

@app.post("/ingest")
def ingest(e: TxnEvent):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO transactions(ts, status, count) VALUES (?, ?, ?)", (e.ts.isoformat(), e.status, e.count))
    conn.commit()

    # consulta rápida e recomendação
    query = """
    WITH per_minute AS (
      SELECT
        substr(ts, 1, 16) AS minute,
        SUM(CASE WHEN status='approved' THEN count ELSE 0 END) AS approved,
        SUM(CASE WHEN status='failed' THEN count ELSE 0 END) AS failed,
        SUM(CASE WHEN status='denied' THEN count ELSE 0 END) AS denied,
        SUM(CASE WHEN status='reversed' THEN count ELSE 0 END) AS reversed
      FROM transactions
      GROUP BY minute
    ),
    with_rate AS (
      SELECT
        minute as ts,
        approved, failed, denied, reversed,
        (failed * 1.0) / NULLIF(approved + failed + denied + reversed, 0) AS failure_rate
      FROM per_minute
    )
    SELECT ts, approved, failed, denied, reversed, failure_rate FROM with_rate ORDER BY ts;
    """
    df = pd.read_sql_query(query, conn, parse_dates=["ts"]) 
    conn.close()

    recommend, details = rolling_alert_recommendation(df, baseline_minutes=60, recent_minutes=5, metric_col="failure_rate", sigma=2.5)

    return {"recommend_alert": recommend, "details": details}