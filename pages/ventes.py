from streamlit_extras.stylable_container import stylable_container

import streamlit as st
from utils.auth_supabase import require_login
from utils.charts import plot_sales_by_category, plot_sales_over_time
from utils.data_loader import load_data
from utils.metrics import average_order_value, top_products, total_revenue


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

require_login()


df = load_data("data/e_commerce_sales.csv")

st.title("Ventes")

# -------------------------------------------------------------------
# ------------------------ SECTION KPI ------------------------------
# -------------------------------------------------------------------

st.subheader("📊 Indicateurs clés")

# ratios équilibrés pour largeur homogène
k1, k2, k3 = st.columns([2.1, 2.3, 3], gap="large")

# ====================== KPI 1 ======================
with k1:
    with stylable_container(
        key="kpi1",
        css_styles=f"""
            {{
                background: #E0F7FA;
                padding: 15px;
                border-radius: 18px;
                text-align: center;
                color: black;
                font-family: 'Inter', sans-serif;
                border: 2px solid rgba(255,255,255,0.35);   /* 🔹 contour léger */
                box-shadow: 0 8px 20px rgba(0, 119, 255, 0.25);  /* 🔹 ombre douce */
            }}
            h2 {{
                
                margin-bottom: 0px;
            }}
            p {{
                font-size: 10rem;
                opacity: .9;
                margin-top: -4px;
                font-family: 'Inter', sans-serif;
                text-align : center;
            }}
        """,
    ):
        st.markdown(
            f"<h2>{total_revenue(df):,.0f} €</h2>" "<p>Chiffre d'affaires total</p>",
            unsafe_allow_html=True,
        )


# ====================== KPI 2 ======================
with k2:
    with stylable_container(
        key="kpi2",
        css_styles=f"""
            {{
                background: #E0F7FA;
                padding: 15px;
                border-radius: 16px;
                text-align: center;
                color: black;
                font-family: 'Inter', sans-serif;
                border: 2px solid rgba(255,255,255,0.35);   /* 🔹 contour léger */
                box-shadow: 0 8px 20px rgba(0, 119, 255, 0.25);  /* 🔹 ombre douce */

            }}
            h2 {{
                
                margin-bottom: -4px;
                
            }}
            p {{
              
                opacity: .9;
                margin-top: -4px;
                text-align : center;
            }}
        """,
    ):
        st.markdown(
            f"<h2>{average_order_value(df):,.2f} €</h2>" "<p>Panier moyen</p>",
            unsafe_allow_html=True,
        )


# ====================== KPI 3 ======================
with k3:
    with stylable_container(
        key="kpi3",
        css_styles=f"""
            {{
                background: #E0F7FA;
                padding: 27px;
                border-radius: 18px;
                text-align: center;
                color: black;
                font-family: 'Inter', sans-serif;
                border: 2px solid rgba(255,255,255,0.35);   /* 🔹 contour léger */
                box-shadow: 0 8px 20px rgba(0, 119, 255, 0.25);  /* 🔹 ombre douce */

            }}
            h2 {{
               
                margin-bottom: -4px;
            }}
            p {{

                opacity: .9;
                text-align : center;
                margin-top: -2px; 
        
            }}
        """,
    ):
        best_product = top_products(df, 1).iloc[0]["product"]
        st.markdown(
            f"<h2>{best_product}</h2>" "<p>Produit le plus vendu</p>",
            unsafe_allow_html=True,
        )


# -------------------------------------------------------------------
# ---------------------- SECTION GRAPHES ----------------------------
# -------------------------------------------------------------------

st.subheader("📈 Visualisation des ventes")

# ----------- GRAPHE AVEC CARD STYLISÉE -----------
with stylable_container(
    key="graph_card",
    css_styles="""
        {
            background: #E3F2FD;
            padding: 25px;
            border-radius: 20px;
            margin-top: 10px;
            box-shadow: 0 5px 25px rgba(0,0,0,0.15);
        }
    """,
):
    st.markdown("### 📌 Ventes par catégorie")
    plot_sales_by_category(df)

with stylable_container(
    key="graph2_card",
    css_styles="""
        {
            background: #E3F2FD;
            padding: 25px;
            border-radius: 20px;
            margin-top: 20px;
            box-shadow: 0 5px 25px rgba(0,0,0,0.15);
        }
    """,
):
    st.markdown("### 📆 Évolution des ventes")
    plot_sales_over_time(df)
