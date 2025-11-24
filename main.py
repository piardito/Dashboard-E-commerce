import streamlit as st
from utils.data_loader import load_data
from utils.style import set_blue_theme

set_blue_theme()

st.set_page_config(page_title="Dashboard E-commerce", layout="wide")
st.title("Dashboard E-commerce")

# Charger les données
df = load_data("data/e_commerce_sales.csv")

# Affichage rapide
st.write("Aperçu des données :")
st.dataframe(df.head())

