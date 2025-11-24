from streamlit_extras.stylable_container import stylable_container

import streamlit as st
from utils.auth_duckdb import require_login
from utils.charts import plot_sales_by_category
from utils.data_loader import load_data

st.markdown(
    """
<style>
.stApp {
    background: linear-gradient(135deg, #D0E8FF, #4DD0E1);  /* bleu clair dégradé */
}
</style>
""",
    unsafe_allow_html=True,
)

# --- Sécurité ---
require_login()


# ----------------------------------------------
# 💠 HEADER STYLISÉ
# ----------------------------------------------
with stylable_container(
    key="header_card",
    css_styles="""
        {

            color: black;   /* TITRE ET TEXTE EN NOIR */
            
        }
        h1 {
            font-size: 1.9rem;
            margin: 0;
            color: black !important;   /* force le titre en noir */
        }
    """,
):
    st.markdown("<h1> Analyses</h1>", unsafe_allow_html=True)


# ----------------------------------------------
# 📌 Sélection de la région (PILLS)
# ----------------------------------------------
df = load_data("data/e_commerce_sales.csv")
regions = sorted(df["region"].unique())

st.subheader("Analyses Régionales")

region = st.pills(
    label="Sélectionner une région :",
    options=regions,
    default=regions[0],
)

df_region = df[df["region"] == region]

st.write(f"Analyse pour la région : **{region}**")

# ----------------------------------------------
# 📊 GRAPHE DANS UNE CARD STYLÉE
# ----------------------------------------------
with stylable_container(
    key="graph_card",
    css_styles="""
        {
            background: #E3F2FD;
            padding: 25px;
            border-radius: 15px;
            margin-top: 10px;
            box-shadow: 0 5px 25px rgba(0,0,0,0.15);
        }
        h3 {
            color: #1565C0;
            margin-bottom: 12px;
            font-size: 1.3rem;
        }
    """,
):
    st.markdown("### 📦 Ventes par catégorie")
    plot_sales_by_category(df_region)
