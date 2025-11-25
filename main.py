import streamlit as st
from streamlit_extras.stylable_container import stylable_container

# Auth Supabase
from utils.auth_supabase import require_login, auth_form, delete_session

# Données
from utils.data_loader import load_data


# ============================================================
#                 CONFIGURATION DE LA PAGE
# ============================================================
st.set_page_config(
    page_title="Dashboard E-commerce",
    layout="wide",
)

# Style global
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #D0E8FF, #4DD0E1);
}
</style>
""", unsafe_allow_html=True)


# ============================================================
#                         HEADER
# ============================================================
with stylable_container(
    key="header",
    css_styles="""
        {
            background: linear-gradient(135deg, #1B4F72, #11608A);
            padding-top: 0.5px;
            padding-bottom: 25px;
            border-radius: 25px;
            color: white;
            margin-bottom: 30px;

            display: flex;
            justify-content: center;
            align-items: flex-start;
            height: 200px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            text-align: center;
        }

        h1 {
            margin: 0;
            font-size: 2.8rem;
            font-weight: 700;
            text-shadow: 1px 1px 4px rgba(0,0,0,0.4);
        }

        @media (max-width: 768px) {
            h1 { font-size: 2rem; }
        }
    """,
):
    st.markdown("<h1>Dashboard E-commerce</h1>", unsafe_allow_html=True)


# ============================================================
#                 AUTHENTIFICATION
# ============================================================

# Déjà connecté → montrer un message + bouton logout
if "user_id" in st.session_state:
    st.success(f"Connecté : user_id = {st.session_state['user_id']}")

    if st.button("Déconnexion"):
        delete_session(st.session_state.get("session_token"))
        st.session_state.clear()
        st.rerun()

else:
    # Pas connecté → afficher le formulaire + stopper l'app
    auth_form()
    st.stop()


# ============================================================
#                 CHARGEMENT DES DONNÉES
# ============================================================
df = load_data("data/e_commerce_sales.csv")

if df is None or df.empty:
    st.error("Impossible de charger les données.")
    st.stop()


# ============================================================
#                AFFICHAGE APERÇU DES DONNÉES
# ============================================================
st.subheader("Aperçu des données")
st.dataframe(df.head())
