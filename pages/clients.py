import plotly.express as px
from streamlit_extras.stylable_container import stylable_container

import streamlit as st
from utils.auth_supabase import require_login
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

# --- Style global ---


# ---------------------------------------------------
# 🔵 HEADER stylisé
# ---------------------------------------------------
with stylable_container(
    key="header_clients",
    css_styles="""
        {
            color: black;
        }
        h1 {
            margin: 0;
            font-size: 2rem;
            font-weight: 700;
        }
    """,
):
    st.markdown("<h1> Clients</h1>", unsafe_allow_html=True)


# ---------------------------------------------------
# 📊 Chargement des données
# ---------------------------------------------------
df = load_data("data/e_commerce_sales.csv")

st.subheader("📈 Analyse Clients")

# ---------------------------------------------------
# 🔹 Répartition des âges (BAR)
# ---------------------------------------------------
age_counts = df["customer_age"].value_counts().reset_index()
age_counts.columns = ["age", "count"]

fig_age = px.bar(
    age_counts,
    x="age",
    y="count",
    title="Répartition par âge",
    labels={"count": "Nombre", "age": "Âge"},
    color="age",
    color_continuous_scale=px.colors.sequential.OrRd,
)

fig_age.update_layout(
    plot_bgcolor="#D8ECFF",
    paper_bgcolor="#D8ECFF",
    font_color="#212529",
    width=100,  # largeur en pixels
    height=400,
)


# ---- Ajout dans une card stylée ----
with stylable_container(
    key="age_card",
    css_styles="""
         {
            background: #E3F2FD;
            padding: 25px;
            border-radius: 20px;
            margin-top: 20px;
            border: 1px solid rgba(255,255,255,0.4);
            box-shadow: 0 15px 40px rgba(0,0,0,0.25);
        }
        
        }
        h3 {
            font-size: 1.3rem;
            margin-bottom: 10px;
            color: #0d47a1;
        }
    """,
):
    st.markdown("### 🎂 Répartition des âges")
    st.plotly_chart(fig_age, use_container_width=True)


# ---------------------------------------------------
# 🔹 Répartition par genre (PIE)
# ---------------------------------------------------
gender_counts = df["customer_gender"].value_counts().reset_index()
gender_counts.columns = ["gender", "count"]

fig_gender = px.pie(
    gender_counts,
    names="gender",
    values="count",
    title="Répartition par genre",
    color_discrete_sequence=["#FDBA74", "#ADD8E6"],
)

fig_gender.update_layout(
    plot_bgcolor="#D8ECFF",
    paper_bgcolor="#D8ECFF",
    font_color="#212529",
    uniformtext_minsize=8,
    margin=dict(l=60, r=140, t=80, b=60),
    legend=dict(
        x=1.05,
        y=1,
        bgcolor="rgba(255,255,255,0)",
    ),
)

# ---- Card stylée PIE ----
with stylable_container(
    key="gender_card",
    css_styles="""
        {
            background: #E3F2FD;
            padding: 25px;
            border-radius: 20px;
            margin-top: 20px;
            border: 1px solid rgba(255,255,255,0.4);
            box-shadow: 0 15px 40px rgba(0,0,0,0.25);
}
        }
        h3 {
            font-size: 1.3rem;
            margin-bottom: 10px;
            color: #0d47a1;
        }
    """,
):
    st.markdown("### 🚻 Répartition par genre")
    st.plotly_chart(fig_gender, use_container_width=True)
