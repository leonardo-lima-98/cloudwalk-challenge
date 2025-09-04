# pages/Incident_Monitor.py

import os
import time
import streamlit as st
import pandas as pd
from model import flag_pos_anomalies, csv_columns_validation, list_checkout_files

UPLOAD_DIR = "data/checkout/"

st.set_page_config(page_title="POS por hora", layout="wide", page_icon="📊", initial_sidebar_state="auto")
st.title("🚦 Incident Monitor")

# Lista inicial de arquivos
files = list_checkout_files()
if "file_index" not in st.session_state:
    st.session_state.file_index = 0  # começa no mais recente

with st.sidebar:
    with st.spinner("Loading..."):
        time.sleep(1.0)
        st.subheader("Envie o CSV :")

        uploaded = st.file_uploader(
            label="colunas: time, today, yesterday, same_day_last_week, avg_last_week, avg_last_month\n",
            type=["csv"], accept_multiple_files=False
        )

        if uploaded:
            filename = uploaded.name
            save_path = os.path.join(UPLOAD_DIR, filename)

            # Salva o arquivo no disco
            with open(save_path, "wb") as f:
                f.write(uploaded.getbuffer())

            st.toast(f"📥 Arquivo salvo em `{save_path}`", icon="✅")

            current_file = save_path
            df = pd.read_csv(current_file)

        else:
            # pega arquivo atual da lista
            current_file = files[st.session_state.file_index]
            df = pd.read_csv(current_file)

        # Atualiza a lista após upload
        files = list_checkout_files()
        file_names = [os.path.basename(f) for f in files]

        # Selectbox sincronizado com file_index
        selected_name = st.selectbox("Escolha o arquivo de checkout:", file_names, index=st.session_state.file_index)
        st.session_state.file_index = file_names.index(selected_name)

        st.divider()


# Navegação por setas
col1, col2, col3 = st.columns([1, 10, 1])
with col1:
    if st.button("⬅️ Anterior", disabled=(st.session_state.file_index >= len(files) - 1)):
        st.session_state.file_index = min(st.session_state.file_index + 1, len(files) - 1)

with col2:
    st.markdown(
        f"<h5 style='text-align: center;'>📄 Arquivo atual: {os.path.basename(current_file)}</h5>",
        unsafe_allow_html=True
    )

with col3:
    if st.button("Próximo ➡️", disabled=(st.session_state.file_index <= 0)):
        st.session_state.file_index = max(st.session_state.file_index - 1, 0)

st.divider()


# Validação + KPIs + gráfico
if csv_columns_validation(df):
    df = flag_pos_anomalies(df)

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Horas com anomalia", int(df["anomaly_flag"].sum()))
    kpi2.metric("Maior z-score", round(df["zscore_today_vs_mean"].abs().max(), 2))
    kpi3.metric("Δ máximo (Hoje - Média)", int(df["delta_vs_mean"].max()))

    st.line_chart(df.set_index("time")[["avg_last_month", "today"]])

    st.dataframe(df, use_container_width=True)

    st.caption("Regra: |z-score| ≥ 2 marca anomalia. O z-score é calculado vs média histórica por hora.")
