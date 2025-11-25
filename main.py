from streamlit_extras.stylable_container import stylable_container

import streamlit as st
#from utils.auth_duckdb import auth_form, delete_session
from utils.auth_supabase import require_login, auth_form, delete_session
from utils.data_loader import load_data

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #D0E8FF, #4DD0E1);  /* bleu clair dégradé */
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------
# Configuration de la page (une seule fois)
# --------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard E-commerce",
    layout="wide",
)


# --------------------------------------------------------------------
# En-tête stylisé
# --------------------------------------------------------------------
with stylable_container(
    key="header",
    css_styles="""
        {
            background: linear-gradient(135deg, #1B4F72, #11608A); /* dégradé bleu */
            padding-top: 0.5px;           /* décalage vers le bas pour le header */
            padding-bottom: 25px;
            border-radius: 25px;
            color: white;
            margin-bottom: 30px;

            display: flex;
            justify-content: center;     /* centrer horizontalement */
            align-items: flex-start;     /* aligner vers le haut */
            height: 200px;               /* hauteur totale du header */
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            text-align: center;
        }

        /* Style du titre */
        h1 {
            margin: 0;
            font-size: 2.8rem;
            font-weight: 700;
            text-shadow: 1px 1px 4px rgba(0,0,0,0.4);
        }

        /* Responsive pour petits écrans */
        @media (max-width: 768px) {
            h1 {
                font-size: 2rem;
            }
        }
    """,
):
    st.markdown("<h1>Dashboard E-commerce</h1>", unsafe_allow_html=True)


# --------------------------------------------------------------------
# Gestion de l’authentification
# --------------------------------------------------------------------
if "user_id" in st.session_state:
    st.success(f"Connecté : user_id = {st.session_state['user_id']}")
    if st.button("Déconnexion"):
        delete_session(st.session_state.get("session_token"))
        st.session_state.clear()
        st.rerun()

else:
    auth_form()
    st.stop()  # Empêche d'afficher les données si non connecté

# --------------------------------------------------------------------
# Chargement des données
# --------------------------------------------------------------------
df = load_data("data/e_commerce_sales.csv")


# --------------------------------------------------------------------
# Aperçu des données
# --------------------------------------------------------------------
st.subheader("Aperçu des données")
st.dataframe(df.head())

