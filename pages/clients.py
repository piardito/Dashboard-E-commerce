import plotly.express as px
from streamlit_extras.stylable_container import stylable_container
import streamlit as st

from utils.auth_supabase import require_login
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
# 🧭 Header
# ----------------------------------------------------------
with stylable_container(
        key="header_clients",
        css_styles="""
        {
            color: black;
        }
        h1 { margin: 0; font-size: 2rem; font-weight: 700; }
    """,
):
    st.markdown("<h1>Clients</h1>", unsafe_allow_html=True)

# ----------------------------------------------------------
# 📊 Load data
# ----------------------------------------------------------
df = load_data("data/e_commerce_sales.csv")

st.subheader("📈 Analyse Clients")

# ----------------------------------------------------------
# 🎨 PALETTE UNIFIÉE (UTILISÉE DANS TOUS LES GRAPHIQUES)
# ----------------------------------------------------------
PALETTE = ["#29B6F6", "#4DD0E1", "#0288D1", "#81D4FA", "#B3E5FC"]

# ----------------------------------------------------------
# 🔹 Répartition des âges (BAR)
# ----------------------------------------------------------
age_counts = df["customer_age"].value_counts().reset_index()
age_counts.columns = ["age", "count"]

fig_age = px.bar(
    age_counts,
    x="age",
    y="count",
    title="Répartition par âge",
    labels={"count": "Nombre", "age": "Âge"},
    color="age",
    color_discrete_sequence=PALETTE,
)

fig_age.update_layout(
    plot_bgcolor="#D8ECFF",
    paper_bgcolor="#D8ECFF",
    font_color="#212529",
    height=400,
)

# ---- Card ----
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

        h3 {
            font-size: 1.3rem;
            margin-bottom: 10px;
            color: #0d47a1;
        }
    """,
):
    st.markdown("### 🎂 Répartition des âges")
    st.plotly_chart(fig_age, use_container_width=True)

# ----------------------------------------------------------
# 🔹 Répartition par genre (PIE)
# ----------------------------------------------------------
gender_counts = df["customer_gender"].value_counts().reset_index()
gender_counts.columns = ["gender", "count"]

fig_gender = px.pie(
    gender_counts,
    names="gender",
    values="count",
    title="Répartition par genre",
    color="gender",
    color_discrete_sequence=["#29B6F6", "#FFB74D"],  # BLEU + ORANGE COMME DASHBOARD
)

fig_gender.update_layout(
    plot_bgcolor="#D8ECFF",
    paper_bgcolor="#D8ECFF",
    font_color="#212529",
    uniformtext_minsize=10,
    margin=dict(l=40, r=40, t=60, b=40),
)

# ---- Card ----
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
        h3 {
            font-size: 1.3rem;
            margin-bottom: 10px;
            color: #0d47a1;
        }
    """,
):
    st.markdown("### 🚻 Répartition par genre")
    st.plotly_chart(fig_gender, use_container_width=True)
