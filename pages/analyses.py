import streamlit as st
from utils.data_loader import load_data
from utils.charts import plot_sales_by_category
from utils.style import set_blue_theme

def show():
    set_blue_theme()

    st.header("Analyses Régionales")
    df = load_data("data/e_commerce_sales.csv")

    region = st.pills("Sélectionner une région", df["region"].unique(),default= df["region"].unique()[0])
    df_region = df[df["region"] == region]

    st.write(f"Analyse pour la région : **{region}**")
    plot_sales_by_category(df_region)
