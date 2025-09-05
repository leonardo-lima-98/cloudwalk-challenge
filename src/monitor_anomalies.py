import pandas as pd

def flag_pos_anomalies(df: pd.DataFrame) -> pd.DataFrame:
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
    df = df.copy()

    # Diferença entre o valor de hoje e a média do último mês
    df["delta_vs_mean"] = df["today"] - df["avg_last_month"]

    # Proxy de desvio padrão:
    # Em vez de usar só o desvio global, pegamos a variância das 3 referências
    # (mesmo dia da semana passada, média da semana e média do mês)
    # Garantimos que nunca seja menor que 1 para evitar divisões por zero
    df["std_proxy"] = (
        df[["same_day_last_week", "avg_last_week", "avg_last_month"]]
        .var(axis=1)   # calcula variância entre as 3 séries
        .clip(lower=1) # evita zero
        .pow(0.5)      # raiz quadrada = desvio padrão
    )

    # Z-score: quantos desvios acima/abaixo da média o valor de hoje está
    df["zscore_today_vs_mean"] = df["delta_vs_mean"] / df["std_proxy"]

    # Flag binária: True se o valor de hoje está a 2 ou mais desvios da média
    df["anomaly_flag"] = df["zscore_today_vs_mean"].abs() >= 2

    return df
