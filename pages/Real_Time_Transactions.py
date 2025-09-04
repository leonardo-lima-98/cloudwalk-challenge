# tab2.py
import os
from click import echo
import streamlit as st
import pandas as pd
import numpy as np #noqa
import time
import sqlite3
from datetime import datetime, timedelta #noqa
from model import flag_pos_anomalies, rolling_alert_recommendation


st.set_page_config(page_title="Monitor de Transações", layout="wide", page_icon="🛰️", initial_sidebar_state="auto")

st.title("🚦 Real_Time_Transactions")


# Using "with" notation
with st.sidebar:
    # Using object notation
    with st.spinner("Loading..."):
        st.sidebar.button(label="🛰️")

st.subheader("Consulta SQL + gráfico e alerta em tempo real")

db_path = st.text_input("Caminho do SQLite (preencha com monitor.db)", "monitor.db")
lookback_min = st.slider("Janela de baseline (min)", 15, 120, 60)
recent_min = st.slider("Janela recente (min)", 1, 20, 5)
fail_sigma = st.slider("Sensibilidade (desvios acima do baseline)", 1.0, 5.0, 2.5, 0.5)

if st.button("Executar consulta e avaliar alerta"):
    conn = sqlite3.connect(db_path)
    query = open("schema.sql").read()
    sql_df = pd.read_sql_query(query, conn, parse_dates=["ts"]) 

    st.line_chart(sql_df.set_index("ts")["failure_rate"])
    st.dataframe(sql_df.tail(30), use_container_width=True)

    # Recomendação de alerta com base no histórico
    recommend, details = rolling_alert_recommendation(
        sql_df,
        baseline_minutes=lookback_min,
        recent_minutes=recent_min,
        metric_col="failure_rate",
        sigma=fail_sigma,
    )
    st.markdown(f"**Recomendação:** {'🚨 ALERTAR' if recommend else '✅ OK'}")
    with st.expander("Detalhes do cálculo"):
        st.json(details)
    conn.close()

st.caption("A consulta SQL agrega por minuto e calcula a taxa de falha. A recomendação compara a janela recente com o baseline histórico usando média e desvio padrão.")