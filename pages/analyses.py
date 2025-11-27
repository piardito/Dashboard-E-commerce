import streamlit as st
from streamlit_extras.stylable_container import stylable_container

from utils.auth_supabase import require_login
from utils.data_loader import load_data
from utils.charts import plot_sales_by_category


# ----------------------------------------------
# 🎨 BACKGROUND GLOBAL
# ----------------------------------------------
st.markdown(
    """
<style>
.stApp {
    background: linear-gradient(135deg, #D0E8FF, #4DD0E1);
}

/* Titres uniformisés */
h1 {
    font-size: 2rem !important;
    color: black !important;
    margin-bottom: 8px;
}

.section-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: black;
    margin-top: 20px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ----------------------------------------------
# 🔐 AUTH OBLIGATOIRE
# ----------------------------------------------
require_login()


# ----------------------------------------------
# 📌 HEADER
# ----------------------------------------------
with stylable_container(
    key="header_card",
    css_styles="""
        {
            background: transparent;
            padding: 5px;
            color: black;
        }
    """,
):
    st.markdown("<h1>Analyses</h1>", unsafe_allow_html=True)


# ----------------------------------------------
# 📊 CHARGEMENT DES DONNÉES
# ----------------------------------------------
df = load_data("data/e_commerce_sales.csv")
regions = sorted(df["region"].unique())


# ----------------------------------------------
# 📍 Sélection de région (pills)
# ----------------------------------------------
st.markdown("<div class='section-title'>Analyses Régionales</div>", unsafe_allow_html=True)

region = st.pills(
    label="Sélectionner une région :",
    options=regions,
    default=regions[0],
)

df_region = df[df["region"] == region]

st.write(f"Analyse pour la région **{region}**")


# ----------------------------------------------
# 📈 GRAPHE : Ventes par catégorie
# ----------------------------------------------
with stylable_container(
    key="graph_region",
    css_styles="""
        {
            background: #E3F2FD;
            padding: 25px;
            border-radius: 20px;
            margin-top: 15px;
            margin-bottom: 40px;
            box-shadow: 0 5px 25px rgba(0,0,0,0.10);
        }
        h3 {
            color: #0D47A1;
            font-size: 1.35rem;
            margin-bottom: 12px;
        }
    """,
):
    st.markdown("### 📦 Ventes par catégorie")
    plot_sales_by_category(df_region)
