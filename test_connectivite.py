import streamlit as st
from supabase import create_client

SUPABASE_URL = st.secrets["supabase"]["url"]
SERVICE_ROLE_KEY = st.secrets["supabase"]["service_role_key"]

try:
    supabase = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)
    res = supabase.table("users").select("*").limit(1).execute()
    st.write("Connexion OK !", res.data)
except Exception as e:
    st.error(f"Impossible de se connecter à Supabase : {e}")
