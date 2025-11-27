import streamlit as st
import time
from streamlit_extras.stylable_container import stylable_container

from utils.auth_supabase import require_login
from utils.charts import plot_sales_by_category, plot_sales_over_time
from utils.data_loader import load_data
from utils.metrics import total_revenue, average_order_value, top_products


# ------------------------------
# BACKGROUND GLOBAL
# ------------------------------
st.markdown(
    """
<style>
.stApp {
    background: linear-gradient(135deg, #D0E8FF, #4DD0E1);
}

/* Centrage vertical + cohérence KPI */
.kpi-value {
    font-size: 1.9rem;
    font-weight: 700;
    margin-bottom: 6px;
}

.kpi-label {
    font-size: 0.95rem;
    opacity: 0.85;
    margin-top: 4px;
}
</style>
""",
    unsafe_allow_html=True,
)

# Auth obligatoire
require_login()

# Load data
df = load_data("data/e_commerce_sales.csv")

# 🏷️ HEADER IDENTIQUE AUX AUTRES PAGES
# ------------------------------------------------------
with stylable_container(
    key="header_ventes",
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
    st.markdown("<h1>Ventes</h1>", unsafe_allow_html=True)


# ---------------------------------------------------
# 🔥 Animation des chiffres
# ---------------------------------------------------
def animate_number(final_value, duration=0.9, steps=35, integer=False, euro=False):
    placeholder = st.empty()
    increment = final_value / steps
    delay = duration / steps
    current = 0

    for _ in range(steps):
        if integer:
            value = f"{int(current):,}".replace(",", " ")
        else:
            value = f"{current:,.2f}".replace(",", " ")

        if euro:
            value += " €"

        placeholder.markdown(
            f"<div class='kpi-value'>{value}</div>",
            unsafe_allow_html=True,
        )
        current += increment
        time.sleep(delay)

    # Valeur finale
    if integer:
        value = f"{int(final_value):,}".replace(",", " ")
    else:
        value = f"{final_value:,.2f}".replace(",", " ")

    if euro:
        value += " €"

    placeholder.markdown(
        f"<div class='kpi-value'>{value}</div>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------
# 🧊 CARDS STYLE
# ---------------------------------------------------
CARD_STYLE = """
{
    background: #E0F7FA;
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    border: 1.5px solid rgba(255,255,255,0.35);
    box-shadow: 0 5px 20px rgba(0,0,0,0.12);
}
"""


# ---------------------------------------------------
# 📊 KPI SECTION (bien alignés)
# ---------------------------------------------------
st.subheader("📊 Indicateurs clés")
k1, k2, k3 = st.columns([1, 1, 1], gap="large")

# KPI 1 – Chiffre d'affaires
with k1:
    with stylable_container(key="kpi1", css_styles=CARD_STYLE):
        animate_number(float(total_revenue(df)), integer=True, euro=True)
        st.markdown("<div class='kpi-label'>Chiffre d'affaires total</div>", unsafe_allow_html=True)

# KPI 2 – Panier moyen
with k2:
    with stylable_container(key="kpi2", css_styles=CARD_STYLE):
        animate_number(float(average_order_value(df)), integer=False, euro=True)
        st.markdown("<div class='kpi-label'>Panier moyen</div>", unsafe_allow_html=True)

# KPI 3 – Produit le plus vendu
with k3:
    with stylable_container(key="kpi3", css_styles=CARD_STYLE):

        # Petite animation de fade-in
        best = top_products(df, 1).iloc[0]["product"]
        ph = st.empty()
        for op in [0.1, 0.3, 0.6, 0.8, 1]:
            ph.markdown(
                f"<div style='font-size:1.5rem;font-weight:700;opacity:{op};'>{best}</div>",
                unsafe_allow_html=True,
            )
            time.sleep(0.05)

        st.markdown("<div class='kpi-label'>Produit le plus vendu</div>", unsafe_allow_html=True)


# ---------------------------------------------------
# 📈 GRAPHES – UN EN DESSOUS DE L'AUTRE
# ---------------------------------------------------

st.subheader("📈 Visualisation des ventes")

# Graphique 1 – Ventes par catégorie
with stylable_container(
    key="graph1",
    css_styles="""
        {
            background: #E3F2FD;
            padding: 25px;
            border-radius: 20px;
            margin-top: 20px;
            box-shadow: 0 5px 25px rgba(0,0,0,0.10);
        }
    """,
):
    st.markdown("### 📌 Ventes par catégorie")
    plot_sales_by_category(df)

# Graphique 2 – Évolution des ventes
with stylable_container(
    key="graph2",
    css_styles="""
        {
            background: #E3F2FD;
            padding: 25px;
            border-radius: 20px;
            margin-top: 25px;
            margin-bottom: 40px;
            box-shadow: 0 5px 25px rgba(0,0,0,0.10);
        }
    """,
):
    st.markdown("### 📆 Évolution des ventes")
    plot_sales_over_time(df)
