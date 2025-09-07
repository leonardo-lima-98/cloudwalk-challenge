import pandas as pd
from pathlib import Path
from src.db.db_utils import close_connection, get_connection

def load_df(db_path: str, query_path: str):
    """
    Carrega dados de um banco SQLite e retorna um DataFrame ordenado cronologicamente.

    A função abre uma conexão com o banco de dados, lê a query SQL de um arquivo,
    executa a consulta e retorna os resultados como um DataFrame Pandas. 
    A coluna `timestamp` é convertida para datetime, os registros são ordenados
    cronologicamente e os índices são resetados. Também são retornados os tempos
    mínimo e máximo encontrados no campo `timestamp`.

    Parâmetros
    ----------
    db_path : str
        Caminho para o arquivo do banco de dados SQLite.
    query_path : str
        Caminho para o arquivo contendo a query SQL a ser executada.

    Retorna
    -------
    sql_df : pandas.DataFrame
        DataFrame resultante da consulta SQL, com a coluna `timestamp` em datetime
        e registros ordenados.
    start_time : pandas.Timestamp
        Menor valor da coluna `timestamp` no DataFrame (tempo inicial).
    end_time : pandas.Timestamp
        Maior valor da coluna `timestamp` no DataFrame (tempo final).

    Nota
    -----
    - Caso ocorra algum erro na leitura ou execução da query, `sql_df` será `None`.
    - A conexão com o banco é fechada automaticamente após a execução da consulta.
    """
    try:
        conn, cursor = get_connection(db_path)
        query = Path(query_path).read_text()
        sql_df = pd.read_sql_query(query, conn, parse_dates=["timestamp"])
        close_connection(conn, cursor)
    except Exception as e:
        sql_df = None

    sql_df = sql_df.copy()
    sql_df["timestamp"] = pd.to_datetime(sql_df["timestamp"])
    sql_df = sql_df.sort_values("timestamp").reset_index(drop=True)

    start_time = sql_df["timestamp"].min()
    end_time = sql_df["timestamp"].max()

    return sql_df, start_time, end_time
