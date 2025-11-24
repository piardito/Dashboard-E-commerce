"""Plotly charts for Streamlit dashboard."""



import pandas as pd
import plotly.express as px

import streamlit as st

COLOR_SEQ = ["#0d6efd", "#06b6d4", "#f59e0b", "#10b981", "#6366f1"]


def plot_sales_by_category(df: pd.DataFrame) -> None:
    sales = df.groupby("category")["total_price"].sum().reset_index()
    fig = px.bar(
        sales,
        x="category",
        y="total_price",
        title="Ventes par catégorie",
        labels={"total_price": "CA (€)", "category": "Catégorie"},
        color="category",
        color_discrete_sequence=COLOR_SEQ,
        text="total_price",
    )
    fig.update_traces(texttemplate="%{text:.2f}€")

    fig.update_layout(
        yaxis_title="CA (€)",
        xaxis_title="Catégorie",
        plot_bgcolor="#cce7ff",
        paper_bgcolor="#cce7ff",
        font_color="#212529",
        uniformtext_minsize=8,
        margin=dict(l=60, r=200, t=80, b=60),  # espace droit suffisant pour la légende
        legend=dict(
            x=1.02,  # décale à droite
            y=1,
            bgcolor="rgba(255,255,255,0)",
            bordercolor="black",
        ),
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_sales_over_time(df: pd.DataFrame) -> None:
    sales_time = df.groupby("date")["total_price"].sum().reset_index()
    fig = px.line(
        sales_time,
        x="date",
        y="total_price",
        title="Ventes dans le temps",
        markers=True,
        line_shape="spline",
        color_discrete_sequence=["#0d6efd"],
    )
    fig.update_layout(
        plot_bgcolor="#cce7ff",
        paper_bgcolor="#cce7ff",
        font_color="#212529",
        xaxis_title="Date",
        yaxis_title="CA (€)",
    )
    st.plotly_chart(fig, use_container_width=True)
