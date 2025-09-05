import pandas as pd
import streamlit as st
import sqlite3
from pathlib import Path


def list_checkout_files(checkout_dir: str):
    """
    Lista os arquivos do diretorio para seleção com st.SelectBox

    Args:
        checkout_dir: diretório de destino (str ou Path)

    Returns:
        Lista de arquivos do diretório
    """
    path = Path(checkout_dir)
    files = [f.name for f in path.iterdir() if f.is_file()]
    files.sort(reverse=True)  # do mais recente pro mais antigo
    return files


def csv_columns_validation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validação do formato de colunas do arquivo CSV.

    Args:
        df: objeto DataFrame carregado pelo Pandas

    Returns:
        Confirmação da validação
    """
    required = {"time", "today", "yesterday", "same_day_last_week", "avg_last_week", "avg_last_month"}
    if not required.issubset(df.columns):
        st.warning(f"CSV deve conter colunas: {sorted(required)}")
        return False
    return True


def save_new_checkout_file(uploaded_file, checkout_dir: str | Path) -> Path:
    """
    Salva o arquivo enviado pelo Streamlit em disco e exibe um toast de confirmação.

    Args:
        uploaded_file: objeto retornado pelo st.file_uploader
        checkout_dir: diretório de destino (str ou Path)

    Returns:
        Path do arquivo salvo
    """
    checkout_dir = Path(checkout_dir)
    checkout_dir.mkdir(parents=True, exist_ok=True)  # garante que a pasta existe

    save_path = checkout_dir / uploaded_file.name

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.toast(f"📥 Arquivo salvo em `{save_path}`", icon="✅")
    return save_path
