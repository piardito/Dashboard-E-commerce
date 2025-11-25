from streamlit_extras.stylable_container import stylable_container
import streamlit as st
import time

from utils.auth_supabase import require_login
from utils.charts import plot_sales_by_category, plot_sales_over_time
from utils.data_loader import load_data
from utils.metrics import average_order_value, top_products, total_revenue


# ------------------------------
# BACKGROUND GÉNÉRAL
# ------------------------------
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

# Auth obligatoire
require_login()


# ------------------------------
# LOAD DATA
# ------------------------------
df = load_data("data/e_commerce_sales.csv")

st.title("Ventes")

# ---------------------------------------------------
# 🔥 Fonction animation des nombres (KPI animés)
# ---------------------------------------------------
def animate_number(final_value, duration=0.9, steps=35, integer=False, euro=False):
    """Affiche un nombre animé, avec option €"""
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
            f"<div style='font-size: 1.8rem; font-weight: 700;'>{value}</div>",
            unsafe_allow_html=True,
        )
        current += increment
        time.sleep(delay)

    # valeur finale
    if integer:
        value = f"{int(final_value):,}".replace(",", " ")
    else:
        value = f"{final_value:,.2f}".replace(",", " ")

    if euro:
        value += " €"

    placeholder.markdown(
        f"<div style='font-size: 1.8rem; font-weight: 700;'>{value}</div>",
        unsafe_allow_html=True,
    )



# ---------------------------------------------------
# ------------------- KPI SECTION -------------------
# ---------------------------------------------------
st.subheader("📊 Indicateurs clés")

k1, k2, k3 = st.columns(3, gap="large")

CARD_STYLE = """
{
    background: #E0F7FA;
    padding: 22px;
    border-radius: 20px;
    text-align: center;
    border: 1.5px solid rgba(255,255,255,0.35);
    box-shadow: 0 5px 20px rgba(0,0,0,0.12);
}
"""

LABEL = "font-size: 0.95rem; opacity: 0.85; margin-top: 6px;"


# ------------- KPI 1 : Chiffre d'affaires -------------
with k1:
    with stylable_container(key="kpi1", css_styles=CARD_STYLE):
        final = float(total_revenue(df))
        animate_number(final, duration=1.0, steps=40, integer=True, euro=True)
        st.markdown(
            f"<div style='{LABEL}'>Chiffre d'affaires total</div>",
            unsafe_allow_html=True,
        )



# ------------- KPI 2 : Panier moyen -------------
with k2:
    with stylable_container(key="kpi2", css_styles=CARD_STYLE):
        final = float(average_order_value(df))
        animate_number(final, duration=1.0, steps=40, integer=False, euro=True)
        st.markdown(
            f"<div style='{LABEL}'>Panier moyen</div>",
            unsafe_allow_html=True,
        )



# ------------- KPI 3 : Produit le plus vendu -------------
with k3:
    with stylable_container(key="kpi3", css_styles=CARD_STYLE):
        best_product = top_products(df, 1).iloc[0]["product"]

        placeholder = st.empty()
        for opacity in [0.1, 0.3, 0.5, 0.8, 1]:
            placeholder.markdown(
                f"<div style='font-size: 1.6rem; font-weight: 700; opacity:{opacity};'>{best_product}</div>",
                unsafe_allow_html=True,
            )
            time.sleep(0.05)

        st.markdown(
            f"<div style='{LABEL}'>Produit le plus vendu</div>",
            unsafe_allow_html=True,
        )



# ---------------------------------------------------
# ----------------- GRAPHES SECTION -----------------
# ---------------------------------------------------

st.subheader("📈 Visualisation des ventes")

# ---------- GRAPH : ventes par catégorie ----------
with stylable_container(
    key="graph1_card",
    css_styles="""
        {
            background: #E3F2FD;
            padding: 25px;
            border-radius: 20px;
            margin-top: 10px;
            box-shadow: 0 5px 25px rgba(0,0,0,0.10);
        }
    """,
):
    st.markdown("### 📌 Ventes par catégorie")
    plot_sales_by_category(df)


# ---------- GRAPH : évolution des ventes ----------
with stylable_container(
    key="graph2_card",
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
    st.markdown("### 📆 Évolution des ventes")
    plot_sales_over_time(df)
