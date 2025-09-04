# model.py

import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

import glob, os

# Pasta onde ficam os checkouts
CHECKOUT_DIR = "data/checkout/"

def list_checkout_files():
    files = glob.glob(os.path.join(CHECKOUT_DIR, "checkout_*.csv"))
    files.sort(reverse=True)  # do mais recente pro mais antigo
    return files


def csv_columns_validation(df: pd.DataFrame):
    required = {"time", "today", "yesterday", "same_day_last_week", "avg_last_week", "avg_last_month"}
    if not required.issubset(df.columns):
        st.warning(f"CSV deve conter colunas: {sorted(required)}")
        return False
    return True


# ---- POS anomalies ----
def flag_pos_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["delta_vs_mean"] = df["today"] - df["avg_last_month"]
    # proxy de desvio com base nas 3 séries
    df["std_proxy"] = (
        df[["same_day_last_week", "avg_last_week", "avg_last_month"]]
        .var(axis=1)
        .clip(lower=1)
        .pow(0.5)
    )
    df["zscore_today_vs_mean"] = df["delta_vs_mean"] / df["std_proxy"]
    df["anomaly_flag"] = df["zscore_today_vs_mean"].abs() >= 2
    return df


# ---- Rolling alert recommendation (rule + score) ----
def rolling_alert_recommendation(
    sql_df: pd.DataFrame,
    baseline_minutes: int = 60,
    recent_minutes: int = 5,
    metric_col: str = "failure_rate",
    sigma: float = 2.5,
):
    if sql_df.empty:
        return False, {"reason": "no-data"}

    sql_df = sql_df.sort_values("ts").copy()
    end = sql_df["ts"].max()
    start_recent = end - pd.Timedelta(minutes=recent_minutes)
    start_base = end - pd.Timedelta(minutes=baseline_minutes + recent_minutes)

    base = sql_df[(sql_df["ts"] >= start_base) & (sql_df["ts"] < start_recent)][metric_col]
    recent = sql_df[sql_df["ts"] >= start_recent][metric_col]

    if len(base) < 5 or len(recent) < 1:
        return False, {"reason": "insufficient-window"}

    mu, sd = base.mean(), base.std(ddof=1) or 1e-6
    recent_mean = recent.mean()

    z = (recent_mean - mu) / sd
    recommend = z >= sigma

    details = {
        "baseline_mean": float(mu),
        "baseline_std": float(sd),
        "recent_mean": float(recent_mean),
        "z_score": float(z),
        "sigma_threshold": float(sigma),
    }
    return bool(recommend), details