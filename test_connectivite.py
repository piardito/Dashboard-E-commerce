import streamlit as st
from supabase import create_client

# Récupération des secrets depuis Streamlit Cloud
SUPABASE_URL = st.secrets["supabase"]["url"]
SERVICE_ROLE_KEY = st.secrets["supabase"]["service_role_key"]

st.title("Test de connexion Supabase")

try:
    # Création du client Supabase
    supabase = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)
    st.success("Client Supabase créé avec succès !")

    # Test lecture de la table users
    res = supabase.table("users").select("*").limit(5).execute()
    if res.data:
        st.success("Lecture de la table 'users' OK !")
        st.write(res.data)
    else:
        st.warning("Aucun utilisateur trouvé ou problème de permissions.")

except Exception as e:
    st.error(f"Erreur lors de la connexion ou lecture : {e}")
