import streamlit as st
import pandas as pd
from src.db.db_utils import (
    init_db,
    populate_db_from_csv
)
from src.monitor_transactions import load_df
from streamlit_autorefresh import st_autorefresh

# --------------------------
# Variaveis de configuração inicial
# --------------------------
db_path = "src/db/monitor.db"
schema_path = "src/db/schema.sql"
csv_path = "data/transactions/transactions.csv"
query_path = "src/db/query.sql"

# --------------------------
# Chamada de funções de inicialização
# --------------------------
init_db(db_path, schema_path)
populate_db_from_csv(db_path, csv_path)
sql_df, start_time, end_time = load_df(db_path, query_path)

# --------------------------
# Configuração da pagina
# --------------------------
st.set_page_config(page_title="Monitor de Transações", layout="wide", page_icon="🚦", initial_sidebar_state="auto")
st.title("🚦 Monitor de Transações")
autorefresh = st_autorefresh(interval=5000, limit=None, key="refresh")

# --------------------------
# Configuração de sessions state
# --------------------------
options = ["approved","failed","denied","reversed","failure_rate"]
if "columns" not in st.session_state:
    st.session_state.columns = options

if "current_time" not in st.session_state:
    st.session_state.current_time = start_time

# --------------------------
# Sidebar
# --------------------------
with st.sidebar:
    with st.spinner("Carregando parâmetros..."):
        st.subheader("Consulta SQL + gráfico e alerta em tempo real")
        st.divider()
        lookback_min = st.slider("Janela baseline (minutos)", min_value=1, max_value=240,
                                 value=60, step=1, help="Janela de tempo que será exibida últimos minutos")
        selected = st.multiselect("Selecione os estados",options,
                                default=st.session_state.columns)
        if len(selected) == 0:
            selected = st.session_state.columns
            st.warning("Você deve selecionar pelo menos um estado!")
        st.session_state.columns = selected

# --------------------------
# Conteúdo principal
# --------------------------
chart_container = st.container()
table_container = st.container()
# Filtra com base no current_time e baseline
current_time = st.session_state.current_time
start_recent = current_time - pd.Timedelta(minutes=lookback_min)
filtered_df = sql_df[(sql_df["timestamp"] >= start_recent) & (sql_df["timestamp"] <= current_time)].copy()
# Mostra o gráfico (se houver dados)
chart_df = filtered_df.set_index("timestamp")[selected]
with chart_container:
    st.line_chart(chart_df, use_container_width=True)
# Mostra a tabela com a janela atual
with table_container:
    st.subheader("Dados na janela atual (ordenado desc.)")
    st.dataframe(filtered_df.sort_values("timestamp", ascending=False), use_container_width=True)
# avança a posição do tempo (se não chegou ao fim)
if st.session_state.current_time < end_time:
    st.session_state.current_time += pd.Timedelta(seconds=500)
else:
    st.session_state.current_time = start_time

