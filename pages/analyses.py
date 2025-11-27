from streamlit_extras.stylable_container import stylable_container
import streamlit as st

from utils.auth_supabase import require_login
from utils.charts import plot_sales_by_category
from utils.data_loader import load_data

# ----------------------------------------------------------
# 🎨 Background global
# ----------------------------------------------------------
st.markdown(
    """
<style>
.stApp {
    background: linear-gradient(135deg, #D0E8FF, #4DD0E1);
}
</style>
""",
    unsafe_allow_html=True,
)

# --- Auth ---
require_login()

# ----------------------------------------------------------
# 🏷️ HEADER IDENTIQUE À VENTES.PY
# ----------------------------------------------------------
with stylable_container(
    key="header_analyses",
    css_styles="""
        {
            padding: 8px 0;
            color: black;
        }
        h1 {
            margin: 0;
            font-size: 2rem;
            font-weight: 700;
            color: black !important;
        }
    """,
):
    st.markdown("<h1>Analyses</h1>", unsafe_allow_html=True)

# ----------------------------------------------------------
# 📊 Load Data
# ----------------------------------------------------------
df = load_data("data/e_commerce_sales.csv")
regions = sorted(df["region"].unique())

st.subheader("🌍 Analyses régionales")

# ----------------------------------------------------------
# 📌 Selection région (pills)
# ----------------------------------------------------------
region = st.pills(
    label="Sélectionner une région :",
    options=regions,
    default=regions[0],
)

df_region = df[df["region"] == region]

st.write(f"Analyse pour la région : **{region}**")

# ----------------------------------------------------------
# 📦 Graphique dans une carte stylée
# ----------------------------------------------------------
with stylable_container(
    key="graph_card",
    css_styles="""
        {
            background: #E3F2FD;
            padding: 25px;
            border-radius: 20px;
            margin-top: 15px;
            box-shadow: 0 5px 25px rgba(0,0,0,0.15);
        }
        h3 {
            color: #1565C0;
            font-size: 1.3rem;
        }
    """,
):
    st.markdown("### 📦 Ventes par catégorie")
    plot_sales_by_category(df_region)
