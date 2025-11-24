"""Load and preprocess e-commerce sales data."""


import pandas as pd

import streamlit as st


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    """Load CSV and compute total price."""
    df: pd.DataFrame = pd.read_csv(path, parse_dates=["date"])
    df["total_price"] = df["unit_price"] * df["quantity"]
    return df
