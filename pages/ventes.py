# ventes.py — version B (modernisée & épurée)
from streamlit_extras.stylable_container import stylable_container
import streamlit as st
import time
from typing import Union

from utils.auth_supabase import require_login
from utils.charts import plot_sales_by_category, plot_sales_over_time
from utils.data_loader import load_data
from utils.metrics import average_order_value, top_products, total_revenue

# ------------------------------
# Global page config & style
# ------------------------------
st.set_page_config(page_title="Ventes — Dashboard", layout="wide")

st.markdown(
    """
<style>
/* Page background */
.stApp {
    background: linear-gradient(180deg, #F6FBFF 0%, #E6F6FF 100%);
    font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
}

/* Small helper styles */
.kpi-value { font-weight: 700; color: #0b3a66; }
.kpi-currency { color: #0b3a66; }
.kpi-label { color: #3a536b; opacity: 0.9; font-size: 0.95rem; }

/* Header */
.header-title {
    font-size: 1.6rem;
    font-weight: 800;
    color: #06283D;
    margin: 0;
}

/* subtle container title */
.section-title { font-size: 1.05rem; color: #06283D; font-weight:700; }

/* reduce default Streamlit padding on wide pages a bit */
[data-testid="stHorizontalBlock"] > div:first-child {
    padding-left: 8px !important;
    padding-right: 8px !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------
# Auth
# ------------------------------
require_login()

# ------------------------------
# Load data
# ------------------------------
df = load_data("data/e_commerce_sales.csv")
if df is None or df.empty:
    st.error("Les données n'ont pas pu être chargées.")
    st.stop()

# ------------------------------
# Small helpers
# ------------------------------
def _fmt_int(n: Union[int, float]) -> str:
    """Format integer with spaces as thousand separator."""
    try:
        return f"{int(n):,}".replace(",", " ")
    except Exception:
        return str(n)


def _fmt_float(n: Union[int, float], precision: int = 2) -> str:
    try:
        return f"{n:,.{precision}f}".replace(",", " ")
    except Exception:
        return str(n)


# Animated number — smoother easing (simple ease-out)
def animate_number(
    final_value: float,
    *,
    duration: float = 0.9,
    steps: int = 35,
    integer: bool = False,
    euro: bool = False,
):
    """Display an animated number in-place. Uses a simple ease-out curve."""
    placeholder = st.empty()

    # generate eased steps (ease out cubic)
    import math

    frames = []
    for i in range(1, steps + 1):
        t = i / steps
        eased = 1 - pow(1 - t, 3)  # cubic ease-out
        frames.append(eased)

    for eased in frames:
        current = final_value * eased
        if integer:
            txt = _fmt_int(current)
        else:
            txt = _fmt_float(current, 2)
        if euro:
            txt = f"{txt} €"

        placeholder.markdown(
            f"<div class='kpi-value' style='font-size:1.9rem'>{txt}</div>",
            unsafe_allow_html=True,
        )
        time.sleep(duration / steps)

    # final (clean)
    if integer:
        final_txt = _fmt_int(final_value)
    else:
        final_txt = _fmt_float(final_value, 2)
    if euro:
        final_txt = f"{final_txt} €"

    placeholder.markdown(
        f"<div class='kpi-value' style='font-size:1.9rem'>{final_txt}</div>",
        unsafe_allow_html=True,
    )


# ------------------------------
# Header
# ------------------------------
with stylable_container(
    key="header",
    css_styles="""
    {
        background: linear-gradient(90deg, rgba(10,84,122,0.08), rgba(17,136,153,0.04));
        padding-top: 10px;
        padding-bottom: 14px;
        border-radius: 14px;
        margin-bottom: 18px;
        border: 1px solid rgba(10,84,122,0.06);
    }
    h1 { margin: 0; }
    """
):
    st.markdown("<h1 class='header-title'>Ventes</h1>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:6px;color:#345;opacity:0.9'>Tableau de bord des ventes & performances</div>", unsafe_allow_html=True)


# ------------------------------
# KPI Section (modernized)
# ------------------------------
st.markdown("<div class='section-title' style='margin-top:18px'>📊 Indicateurs clés</div>", unsafe_allow_html=True)

# Use slightly different column ratios for nicer visual balance
c1, c2, c3 = st.columns([2.1, 2.1, 3.2], gap="large")

KPI_CARD = """
{
    background: rgba(255,255,255,0.85);
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    border: 1px solid rgba(10,84,122,0.06);
    box-shadow: 0 6px 22px rgba(10,84,122,0.06);
}
"""

SMALL_LABEL_STYLE = "font-size:0.95rem; color:#334e68; opacity:0.95; margin-top:8px;"


with c1:
    with stylable_container(key="kpi_revenue", css_styles=KPI_CARD):
        st.markdown("<div style='font-size:0.95rem;color:#0a4d7a;font-weight:700;margin-bottom:6px'>💰 Chiffre d'affaires</div>", unsafe_allow_html=True)
        final_ca = float(total_revenue(df))
        animate_number(final_ca, duration=1.0, steps=45, integer=True, euro=True)
        st.markdown(f"<div style='{SMALL_LABEL_STYLE}'>Total sur la période</div>", unsafe_allow_html=True)


with c2:
    with stylable_container(key="kpi_aov", css_styles=KPI_CARD):
        st.markdown("<div style='font-size:0.95rem;color:#0a4d7a;font-weight:700;margin-bottom:6px'>🛒 Panier moyen</div>", unsafe_allow_html=True)
        final_aov = float(average_order_value(df))
        animate_number(final_aov, duration=1.0, steps=45, integer=False, euro=True)
        st.markdown(f"<div style='{SMALL_LABEL_STYLE}'>Valeur moyenne par commande</div>", unsafe_allow_html=True)


with c3:
    with stylable_container(key="kpi_top", css_styles=KPI_CARD):
        st.markdown("<div style='font-size:0.95rem;color:#0a4d7a;font-weight:700;margin-bottom:6px'>🏆 Produit phare</div>", unsafe_allow_html=True)
        best_product = top_products(df, 1).iloc[0]["product"]
        # smaller typography for long product names
        display_name = best_product if len(best_product) <= 26 else best_product[:23] + "..."
        # subtle fade-in animation
        ph = st.empty()
        for opacity in [0.15, 0.35, 0.6, 0.85, 1]:
            ph.markdown(f"<div style='font-size:1.4rem;font-weight:700;opacity:{opacity};color:#0b3a66'>{display_name}</div>", unsafe_allow_html=True)
            time.sleep(0.04)
        st.markdown(f"<div style='{SMALL_LABEL_STYLE}'>Produit le plus vendu</div>", unsafe_allow_html=True)


# ------------------------------
# Graphs Section (keep graphs' backgrounds untouched)
# ------------------------------
st.markdown("<div class='section-title' style='margin-top:22px'>📈 Visualisation des ventes</div>", unsafe_allow_html=True)

g1, g2 = st.columns([1, 1], gap="large")

with g1:
    with stylable_container(
        key="graph_card_1",
        css_styles="""
        {
            background: rgba(255,255,255,0.90);
            padding: 18px;
            border-radius: 14px;
            border: 1px solid rgba(10,84,122,0.04);
            box-shadow: 0 6px 22px rgba(10,84,122,0.04);
        }
        h3 { margin: 0 0 8px 0; color:#0b3a66; font-weight:700; }
        """
    ):
        st.markdown("<h3 style='font-size:1.05rem'>📌 Ventes par catégorie</h3>", unsafe_allow_html=True)
        # Note: plot_sales_by_category should render same visuals as before
        plot_sales_by_category(df)

with g2:
    with stylable_container(
        key="graph_card_2",
        css_styles="""
        {
            background: rgba(255,255,255,0.90);
            padding: 18px;
            border-radius: 14px;
            border: 1px solid rgba(10,84,122,0.04);
            box-shadow: 0 6px 22px rgba(10,84,122,0.04);
        }
        h3 { margin: 0 0 8px 0; color:#0b3a66; font-weight:700; }
        """
    ):
        st.markdown("<h3 style='font-size:1.05rem'>📆 Évolution des ventes</h3>", unsafe_allow_html=True)
        plot_sales_over_time(df)
