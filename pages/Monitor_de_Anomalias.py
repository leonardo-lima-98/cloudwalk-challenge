import time
import streamlit as st
import pandas as pd
from pathlib import Path
from src.monitor_anomalies import flag_pos_anomalies_line_chart, flag_pos_anomalies_dataframe
from src.utils import csv_columns_validation, list_checkout_files, save_new_checkout_file

# --------------------------
# Variaveis de configuração inicial
# --------------------------
CHECKOUT_DIR = "data/checkout/"

# --------------------------
# Configuração da pagina
# --------------------------
st.set_page_config(page_title="Monitor de Anomalias", layout="wide", page_icon="📊", initial_sidebar_state="auto")
st.title("📊 Monitor de Anomalias")

# --------------------------
# Configuração de sessions state
# --------------------------
files = list_checkout_files(CHECKOUT_DIR)
if "file_index" not in st.session_state:
    st.session_state.file_index = 0  

# --------------------------
# Sidebar
# --------------------------
with st.sidebar:
    with st.spinner("Loading..."):
        time.sleep(1.0)
        st.subheader("Envie o CSV :")

        uploaded = st.file_uploader(
            label="colunas: time, today, yesterday, same_day_last_week, avg_last_week, avg_last_month\n",
            type=["csv"], accept_multiple_files=False
        )

        if uploaded:
            save_path = save_new_checkout_file(uploaded, CHECKOUT_DIR)
            df = pd.read_csv(save_path)

        else:
            # pega arquivo atual da lista
            current_file = files[st.session_state.file_index]
            df = pd.read_csv(Path(CHECKOUT_DIR,current_file))

        # Atualiza a lista após upload
        files = list_checkout_files(CHECKOUT_DIR)

        # Selectbox sincronizado com file_index
        selected_name = st.selectbox("Escolha o arquivo de checkout:", files, index=st.session_state.file_index)
        st.session_state.file_index = files.index(selected_name)

        st.divider()


# --------------------------
# Conteúdo principal
# --------------------------
# Navegação por setas
col1, col2, col3 = st.columns([1, 10, 1])
with col1:
    if st.button("⬅️ Anterior", disabled=(st.session_state.file_index >= len(files) - 1)):
        st.session_state.file_index = min(st.session_state.file_index + 1, len(files) - 1)

with col2:
    st.markdown(
        f"<h5 style='text-align: center;'>📄 Arquivo atual: {current_file}</h5>",
        unsafe_allow_html=True
    )

with col3:
    if st.button("Próximo ➡️", disabled=(st.session_state.file_index <= 0)):
        st.session_state.file_index = max(st.session_state.file_index - 1, 0)

st.divider()


# Validação + KPIs + gráfico
if csv_columns_validation(df):
    df_line_chart = flag_pos_anomalies_line_chart(df)
    df_dataframe = flag_pos_anomalies_dataframe(df)

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Horas com anomalia", int(df_line_chart["anomaly_flag"].sum()))
    kpi2.metric("Maior z-score", round(df_line_chart["zscore_today_vs_mean"].abs().max(), 2))
    kpi3.metric("Δ máximo (Hoje - Média)", int(df_line_chart["delta_vs_mean"].max()))

    st.line_chart(df_line_chart.set_index("time")[["avg_last_month", "today"]])

    st.dataframe(df_dataframe, use_container_width=True, hide_index=True)

    st.caption("Regra: |z-score| ≥ 2 marca anomalia. O z-score é calculado vs média histórica por hora.")
