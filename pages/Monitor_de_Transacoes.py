import streamlit as st
import pandas as pd
from pathlib import Path
from src.db.db_utils import (
    close_connection,
    init_db,
    get_connection,
    populate_db_from_csv
)
from src.monitor_transactions import rolling_alert_recommendation
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

# --------------------------
# Configuração da pagina
# --------------------------
st.set_page_config(page_title="Monitor de Transações", layout="wide", page_icon="🚦", initial_sidebar_state="auto")
st.title("🚦 Monitor de Transações")
autorefresh = st_autorefresh(interval=10000, limit=None, key="refresh")

# --------------------------
# Sidebar
# --------------------------
with st.sidebar:
    with st.spinner("Carregando parâmetros..."):
        st.subheader("Consulta SQL + gráfico e alerta em tempo real")
        st.divider()
        options = ["approved","failed","denied","reversed","failure_rate"]
        if "columns" not in st.session_state:
            st.session_state.columns = ["approved"]

        lookback_min = st.slider("Janela de baseline (min)", 15, 240, 60)
        selected = st.multiselect("Selecione os estados",options,
                                default=st.session_state.columns)
        if len(selected) == 0:
            selected = st.session_state.columns
            st.warning("Você deve selecionar pelo menos um estado!")
        st.session_state.columns = selected
try:
    conn, cursor = get_connection(db_path)
    query = Path(query_path).read_text()
    sql_df = pd.read_sql_query(query, conn, parse_dates=["timestamp"])
    close_connection(conn, cursor)
    # sql_df = pd.read_csv(csv_path)
except Exception as e:
    st.toast(f"Erro ao executar consulta: {e}")
    sql_df = None

# --------------------------
# Conteúdo principal
# --------------------------
if sql_df is None:
    st.subheader("Execute a consulta SQL para visualizar os dados.")
elif sql_df.empty:
    st.error("A consulta SQL para visualizar os dados retornou vazio.")
else:
    # Calcula recomendação
    sql_df_dated = rolling_alert_recommendation(
        sql_df,
        baseline_minutes=lookback_min
    )
    # Mostra gráfico com threshold
    chart_df = sql_df_dated.set_index("timestamp")[selected]
    st.line_chart(chart_df, use_container_width=True)

    # Tabela
    st.dataframe(sql_df_dated.sort_index(ascending=False), use_container_width=True, hide_index=True)

