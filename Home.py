# app.py

import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Desafio CloudWalk", layout="wide", page_icon="🏠")
st.title("Home")

# Criando abas
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Visão Geral", "📊 Monitor de Anomalias", "🚦 Monitor de Transações", "Informações Gerais"])

with tab1:
    st.write("### Documentação do Projeto")
    st.write("👉 Aqui você coloca os gráficos, métricas, tabelas...")

with tab2:
    st.write("### Documentação do Projeto")
    docs_path = Path("docs/anomaly_monitor.md")
    if docs_path.exists():
        st.markdown(docs_path.read_text(), unsafe_allow_html=True)
    else:
        st.warning("❌ Arquivo de documentação não encontrado.")

with tab3:
    st.write("### Documentação do Projeto")
    st.write("👉 Aqui você coloca os gráficos, métricas, tabelas...")

with tab4:
    st.write("### Documentação do Projeto")
    st.write("👉 Aqui você coloca os gráficos, métricas, tabelas...")

