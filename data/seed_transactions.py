# seed_transactions.py

# Gera dados sintéticos em monitor.db para brincar na aba 2
import sqlite3
import numpy as np
from datetime import datetime, timedelta
np.random.seed(7)


conn = sqlite3.connect("monitor.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS transactions(ts TEXT, status TEXT, count INTEGER)")


now = datetime.utcnow().replace(second=0, microsecond=0)
for i in range(180):
    ts = (now - timedelta(minutes=180-i)).isoformat()
    lam = {"approved":80, "failed":5, "denied":8, "reversed":2}
    if i >= 150: # últimas 30 min com falhas maiores
        lam["failed"] = 20
    for s, l in lam.items():
        cur.execute("INSERT INTO transactions VALUES (?,?,?)", (ts, s, int(np.random.poisson(l))))


conn.commit(); conn.close()
print("monitor.db populado")