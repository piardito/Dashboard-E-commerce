import streamlit as st
from utils.data_loader import load_data
from utils.metrics import total_revenue, average_order_value, top_products
from utils.charts import plot_sales_by_category, plot_sales_over_time
from utils.style import set_blue_theme

def show():
    set_blue_theme()

    st.header("Analyse des Ventes")
    df = load_data("data/e_commerce_sales.csv")

    # KPI
    col1, col2, col3 = st.columns([0.8,0.8,1.6])
    col1.metric("Chiffre d'affaires total", f"{total_revenue(df):,.1f} €")
    col2.metric("Panier moyen", f"{average_order_value(df):,.2f} €")
    col3.metric("Produit le plus vendu", top_products(df,1).iloc[0]['product'])

    # Graphiques
    plot_sales_by_category(df)
    plot_sales_over_time(df)
