import sqlite3
import pandas as pd
from pathlib import Path


def get_connection(db_path: str):
    """Abre conexão com o SQLite e retorna conn, cursor."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor


def close_connection(conn, cursor):
    """Fecha cursor e conexão."""
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def init_db(db_path: str, schema_path: str):
    """
    Inicializa o banco de dados.
    - Cria o arquivo se não existir.
    - Executa o schema.sql.
    """
    conn, cursor = get_connection(db_path)
    schema_sql = Path(schema_path).read_text()
    cursor.executescript(schema_sql)
    conn.commit()
    close_connection(conn, cursor)


def is_db_empty(db_path: str) -> bool:
    """Valida se a tabela está vazia."""
    conn, cursor = get_connection(db_path)
    cursor.execute(f"SELECT COUNT(*) FROM transactions")
    count = cursor.fetchone()[0]
    close_connection(conn, cursor)
    return count == 0


def populate_db_from_csv(db_path: str, csv_path: str):
    """
    Popula o banco de dados a partir de um CSV,
    apenas se a tabela estiver vazia.
    """
    if not Path(csv_path).exists():
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {csv_path}")

    if is_db_empty(db_path):
        df = pd.read_csv(csv_path)

        conn, cursor = get_connection(db_path)
        df.to_sql('transactions', conn, if_exists="append", index=False)
        conn.commit()
        close_connection(conn, cursor)
        print(f"✅ Banco populado com {len(df)} registros de {csv_path}")
    else:
        print("⚠️ Banco já possui dados, não foi populado novamente.")
