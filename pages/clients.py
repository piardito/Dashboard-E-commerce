import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.style import set_blue_theme

def show():
    set_blue_theme()


    st.header("Analyse Clients")
    df = load_data("data/e_commerce_sales.csv")

    # Age distribution
    age_counts = df["customer_age"].value_counts().reset_index()
    age_counts.columns = ["age", "count"]
    fig_age = px.bar(
        age_counts,
        x="age", y="count",
        title="Répartition par âge",
        labels={"count":"Nombre","age":"Âge"},
        color="age",
        color_discrete_sequence=px.colors.sequential.Teal
    )
    st.plotly_chart(fig_age, use_container_width=True)

    # Gender distribution
    gender_counts = df["customer_gender"].value_counts().reset_index()
    gender_counts.columns = ["gender","count"]
    fig_gender = px.pie(
        gender_counts,
        names="gender",
        values="count",
        title="Répartition par genre",
        color_discrete_sequence=["#0d6efd","#06b6d4"]
    )
    st.plotly_chart(fig_gender, use_container_width=True)
