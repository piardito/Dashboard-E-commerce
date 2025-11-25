from streamlit_extras.stylable_container import stylable_container
import streamlit as st
from utils.auth_supabase import require_login
from utils.charts import plot_sales_by_category, plot_sales_over_time
from utils.data_loader import load_data
from utils.metrics import average_order_value, top_products, total_revenue


# -------------------------------------------------------------------
# ------------------------ STYLE GLOBAL ------------------------------
# -------------------------------------------------------------------

st.markdown(
    """
<style>
/* ---- Background de Dashboard Premium ---- */
.stApp {
    background: linear-gradient(135deg, #eef7ff, #d9f1ff);
    font-family: "Inter", sans-serif;
}

/* ---- Titres ---- */
h1, h2, h3 {
    font-family: "Inter", sans-serif !important;
    font-weight: 700 !important;
}

/* ---- Petits textes ---- */
p, div, span {
    font-family: "Inter", sans-serif !important;
}

/* ---- Amélioration de la taille des KPI ---- */
.kpi-value {
    font-size: 2.7rem;
    font-weight: 700;
    margin-bottom: -8px;
}

.kpi-label {
    font-size: 0.95rem;
    color: #4a4a4a;
    opacity: 0.9;
}

</style>
""",
    unsafe_allow_html=True,
)

require_login()

df = load_data("data/e_commerce_sales.csv")

st.title("📊 Tableau de bord — Ventes")

# -------------------------------------------------------------------
# ------------------------ SECTION KPI ------------------------------
# -------------------------------------------------------------------

st.markdown("### 🔍 Indicateurs clés")

k1, k2, k3 = st.columns([2, 2, 3], gap="large")


# ---- TEMPLATE DE STYLE GLASSMORPHISM ----
CARD_STYLE = """
{
    background: rgba(255, 255, 255, 0.55);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.4);
    box-shadow: 0 4px 25px rgba(0, 0, 0, 0.12);
    text-align: center;
}
"""

ICON_STYLE = "font-size: 26px; margin-bottom: 6px; color:#0A66C2;"


# ====================== KPI 1 ======================
with k1:
    with stylable_container(key="kpi1", css_styles=CARD_STYLE):

        st.markdown(f"<div style='{ICON_STYLE}'>💰</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='kpi-value'>{total_revenue(df):,.0f} €</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<div class='kpi-label'>Chiffre d'affaires total</div>", unsafe_allow_html=True)


# ====================== KPI 2 ======================
with k2:
    with stylable_container(key="kpi2", css_styles=CARD_STYLE):

        st.markdown(f"<div style='{ICON_STYLE}'>🛒</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='kpi-value'>{average_order_value(df):,.2f} €</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<div class='kpi-label'>Panier moyen</div>", unsafe_allow_html=True)


# ====================== KPI 3 ======================
with k3:
    with stylable_container(key="kpi3", css_styles=CARD_STYLE):

        best_product = top_products(df, 1).iloc[0]["product"]

        st.markdown(f"<div style='{ICON_STYLE}'>🏆</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='kpi-value'>{best_product}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<div class='kpi-label'>Produit le plus vendu</div>", unsafe_allow_html=True)



# -------------------------------------------------------------------
# ---------------------- SECTION GRAPHIQUES --------------------------
# -------------------------------------------------------------------

st.markdown("### 📈 Visualisation des performances")


GRAPH_CARD = """
{
    background: rgba(255,255,255,0.6);
    padding: 30px;
    border-radius: 20px;
    margin-top: 20px;
    box-shadow: 0 3px 20px rgba(0,0,0,0.12);
    border: 1px solid rgba(255,255,255,0.35);
}
"""


# ----------- GRAPHE 1 -----------
with stylable_container(key="graph_card_1", css_styles=GRAPH_CARD):
    st.markdown("#### 📦 Répartition des ventes par catégorie")
    plot_sales_by_category(df)


# ----------- GRAPHE 2 -----------
with stylable_container(key="graph_card_2", css_styles=GRAPH_CARD):
    st.markdown("#### 📅 Évolution des ventes dans le temps")
    plot_sales_over_time(df)
