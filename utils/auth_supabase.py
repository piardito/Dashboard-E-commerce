import datetime
import secrets
import pandas as pd
from supabase import create_client
import streamlit as st
import hashlib

# -----------------------------
# CONFIGURATION SUPABASE
# -----------------------------
SUPABASE_URL = st.secrets["supabase"]["url"]
SERVICE_ROLE_KEY = st.secrets["supabase"]["service_role_key"]
supabase = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

# -----------------------------
# CONSTANTES HASH
# -----------------------------
PBKDF2_ITER = 200_000
HASH_NAME = "sha256"

# -----------------------------
# HASH DUCKDB EXISTANT
# -----------------------------
def _hash_password(password: str, salt: str) -> str:
    """Hash du mot de passe compatible avec l’ancien DuckDB"""
    return hashlib.pbkdf2_hmac(
        HASH_NAME, password.encode(), bytes.fromhex(salt), PBKDF2_ITER
    ).hex()

def verify_password(stored_hash: str, salt_hex: str, password: str) -> bool:
    """Vérifie le mot de passe contre le hash et le sel stocké"""
    return secrets.compare_digest(_hash_password(password, salt_hex), stored_hash)

# -----------------------------
# UTILISATEURS
# -----------------------------
def get_user_by_email(email: str):
    """Récupère un utilisateur depuis Supabase par email"""
    res = supabase.table("users").select("*").eq("email", email.lower()).execute()
    data = res.data
    if data:
        return data[0]
    return None

def create_user(email: str, username: str, password: str):
    """Crée un utilisateur (hash + sel)"""
    salt = secrets.token_hex(16)  # 16 bytes
    password_hash = _hash_password(password, salt)
    user = {
        "email": email.lower(),
        "username": username,
        "password_hash": password_hash,
        "salt": salt,
        "created_at": datetime.datetime.utcnow().isoformat(),
    }
    supabase.table("users").insert(user).execute()
    return get_user_by_email(email)

def authenticate_user(email: str, password: str):
    """Authentifie un utilisateur"""
    user = get_user_by_email(email)
    if user and verify_password(user["password_hash"], user["salt"], password):
        return user
    return None

# -----------------------------
# SESSIONS
# -----------------------------
SESSION_DURATION_HOURS = 24 * 7  # 7 jours

def create_session(user_id: int):
    token = secrets.token_urlsafe(32)
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=SESSION_DURATION_HOURS)
    session = {
        "token": token,
        "user_id": user_id,
        "created_at": datetime.datetime.utcnow().isoformat(),
        "expires_at": expires_at.isoformat(),
    }
    supabase.table("sessions").insert(session).execute()
    st.session_state["session_token"] = token
    st.session_state["user_id"] = user_id
    return token

def get_session(token: str):
    res = supabase.table("sessions").select("*").eq("token", token).execute()
    data = res.data
    if not data:
        return None
    session = data[0]
    expires_at = pd.to_datetime(session["expires_at"])
    if datetime.datetime.utcnow() > expires_at:
        delete_session(token)
        return None
    return session

def delete_session(token: str):
    if token:
        supabase.table("sessions").delete().eq("token", token).execute()
    st.session_state.pop("session_token", None)
    st.session_state.pop("user_id", None)

def restore_session():
    if "session_token" not in st.session_state:
        res = supabase.table("sessions").select("*").order("created_at", desc=True).limit(1).execute()
        if res.data:
            session = res.data[0]
            expires_at = pd.to_datetime(session["expires_at"])
            if datetime.datetime.utcnow() < expires_at:
                st.session_state["session_token"] = session["token"]
                st.session_state["user_id"] = session["user_id"]

def require_login():
    restore_session()
    token = st.session_state.get("session_token")
    if not token or not get_session(token):
        st.warning("Tu dois te connecter pour accéder à cette page.")
        st.stop()

# -----------------------------
# FORMULAIRE STREAMLIT
# -----------------------------
def auth_form():
    tab_login, tab_signup = st.tabs(["Connexion", "Créer un compte"])

    with tab_login:
        st.subheader("Connexion")
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("Email")
            password = st.text_input("Mot de passe", type="password")
            submitted = st.form_submit_button("Se connecter")
            if submitted:
                user = authenticate_user(email, password)
                if user:
                    create_session(user["id"])
                    st.success(f"Connecté en tant que {user['username']}")
                    st.rerun()
                else:
                    st.error("Email ou mot de passe incorrect.")

    with tab_signup:
        st.subheader("Créer un compte")
        with st.form("signup_form", clear_on_submit=True):
            email = st.text_input("Email")
            username = st.text_input("Nom d'utilisateur")
            password = st.text_input("Mot de passe", type="password")
            password2 = st.text_input("Confirmer mot de passe", type="password")
            submitted = st.form_submit_button("Créer un compte")
            if submitted:
                if not email or not username or not password:
                    st.error("Remplis tous les champs.")
                elif password != password2:
                    st.error("Les mots de passe ne correspondent pas.")
                elif get_user_by_email(email):
                    st.error("Un compte existe déjà pour cet email.")
                else:
                    user = create_user(email, username, password)
                    if user:
                        st.success("Compte créé ! Connecte-toi maintenant.")
                        st.rerun()
                    else:
                        st.error("Erreur lors de la création du compte.")
