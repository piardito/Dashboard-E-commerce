import plotly.express as px
from streamlit_extras.stylable_container import stylable_container
import streamlit as st
from utils.auth_supabase import require_login
from utils.data_loader import load_data

# ---------------------------------------------------
# 🔵 Background général
# ---------------------------------------------------
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

# Sécurité
require_login()

# ---------------------------------------------------
# 🔵 HEADER
# ---------------------------------------------------
with stylable_container(
    key="header_clients",
    css_styles="""
        {
            color: black;
            padding: 5px;
        }
        h1 {
            margin: 0;
            font-size: 2rem;
            font-weight: 700;
        }
    """,
):
    st.markdown("<h1>👥 Clients</h1>", unsafe_allow_html=True)


# ---------------------------------------------------
# 📊 Chargement des données
# ---------------------------------------------------
df = load_data("data/e_commerce_sales.csv")

st.subheader("📈 Analyse des clients")

# ---------------------------------------------------
# 🔹 Graphique 1 — Âges
# ---------------------------------------------------
age_counts = df["customer_age"].value_counts().reset_index()
age_counts.columns = ["age", "count"]

fig_age = px.bar(
    age_counts,
    x="age",
    y="count",
    title="Répartition par âge",
    labels={"count": "Nombre de clients", "age": "Âge"},
    color="age",
    color_continuous_scale=px.colors.sequential.OrRd,
)

fig_age.update_layout(
    font_color="#212529",
    margin=dict(l=20, r=20, t=60, b=20),
)

# ---- Card stylée matching VENTES ----
with stylable_container(
    key="age_card",
    css_styles="""
        {
            background: #E0F7FA;
            padding: 25px;
            border-radius: 20px;
            margin-top: 15px;
            border: 2px solid rgba(255,255,255,0.35);
            box-shadow: 0 8px 20px rgba(0, 119, 255, 0.25);
        }
        h3 {
            font-size: 1.35rem;
            font-weight: 700;
            color: #01579b;
            margin-bottom: 10px;
        }
    """,
):
    st.markdown("### 🎂 Répartition des âges")
    st.plotly_chart(fig_age, use_container_width=True)


# ---------------------------------------------------
# 🔹 Graphique 2 — Genre
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
    font_color="#212529",
    margin=dict(l=20, r=20, t=60, b=20),
    legend=dict(x=0.9, y=1),
)

# ---- Card stylée matching VENTES ----
with stylable_container(
    key="gender_card",
    css_styles="""
        {
            background: #E0F7FA;
            padding: 25px;
            border-radius: 20px;
            margin-top: 20px;
            border: 2px solid rgba(255,255,255,0.35);
            box-shadow: 0 8px 20px rgba(0, 119, 255, 0.25);
        }
        h3 {
            font-size: 1.35rem;
            font-weight: 700;
            color: #01579b;
        }
    """,
):
    st.markdown("### 🚻 Répartition par genre")
    st.plotly_chart(fig_gender, use_container_width=True)
