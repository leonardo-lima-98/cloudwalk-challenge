import pandas as pd

# ---- Rolling alert recommendation (rule + score) ----
def rolling_alert_recommendation(
    sql_df: pd.DataFrame,
    baseline_minutes: int
    ):
    """
    Detecta possíveis anomalias nos dados de checkout com base em comparação estatística.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame contendo as colunas:
        - today
        - same_day_last_week
        - avg_last_week
        - avg_last_month

    Retorna
    -------
    pd.DataFrame
        O mesmo DataFrame enriquecido com as colunas:
        - delta_vs_mean: diferença entre hoje e a média do último mês
        - std_proxy: desvio padrão proxy baseado no histórico (sem deixar zero)
        - zscore_today_vs_mean: padronização estatística (delta / desvio)
        - anomaly_flag: flag True/False se é anomalia
    """
    if sql_df.empty:
        return False, {"reason": "no-data"}

    sql_df = sql_df.sort_values("timestamp")
    end = sql_df["timestamp"].max()
    start_recent = end - pd.Timedelta(minutes=baseline_minutes)
    sql_df = sql_df[pd.to_datetime(sql_df['timestamp']) >= start_recent]

    return sql_df

