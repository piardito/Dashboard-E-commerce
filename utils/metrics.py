"""Compute KPIs."""

import pandas as pd


def total_revenue(df: pd.DataFrame) -> float:
    return float(df["total_price"].sum())


def average_order_value(df: pd.DataFrame) -> float:
    return float(df["total_price"].mean())


def top_products(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    return (
        df.groupby("product")["total_price"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )
