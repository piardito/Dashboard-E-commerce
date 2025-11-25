# utils/auth_supabase.py
import datetime
import secrets
import streamlit as st
from supabase import create_client
from passlib.hash import pbkdf2_sha256

# -------------------------
# Connexion Supabase
# -------------------------
supabase = create_client(
    st.secrets["supabase"]["url"],
    st.secrets["supabase"]["service_role_key"]
)

# -------------------------
# Paramètres
# -------------------------
TOKEN_BYTES = 32
SESSION_DURATION_HOURS = 24 * 7  # 7 jours

# -------------------------
# Utilitaires utilisateurs
# -------------------------
def hash_password(password: str) -> str:
    """Hache un mot de passe avec pbkdf2_sha256"""
    return pbkdf2_sha256.hash(password)

def verify_password(password: str, hash_: str) -> bool:
    return pbkdf2_sha256.verify(password, hash_)

def get_user_by_email(email: str):
    """Récupère un utilisateur par email"""
    resp = supabase.table("users").select("*").eq("email", email).execute()
    data = resp.data
    return data[0] if data else None

def create_user(email: str, username: str, password: str):
    """Créer un utilisateur et le stocker dans Supabase"""
    if get_user_by_email(email):
        return None  # déjà existant
    password_hash = hash_password(password)
    user = {
        "email": email.lower(),
        "username": username,
        "password_hash": password_hash,
        "role": "user",
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    supabase.table("users").insert(user).execute()
    return get_user_by_email(email)

def authenticate_user(email: str, password: str):
    """Vérifie l'email et mot de passe"""
    user = get_user_by_email(email)
    if user and verify_password(password, user["password_hash"]):
        return {"id": user["id"], "email": user["email"], "username": user["username"]}
    return None

# -------------------------
# Gestion des sessions
# -------------------------
def create_session(user_id: int):
    token = secrets.token_urlsafe(TOKEN_BYTES)
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=SESSION_DURATION_HOURS)
    session = {
        "token": token,
        "user_id": user_id,
        "expires_at": expires_at.isoformat(),
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    supabase.table("sessions").insert(session).execute()
    st.session_state["session_token"] = token
    st.session_state["user_id"] = user_id
    return token

def get_session(token: str):
    """Récupère et valide la session"""
    resp = supabase.table("sessions").select("*").eq("token", token).execute()
    rows = resp.data
    if not rows:
        return None
    row = rows[0]
    expires_at = datetime.datetime.fromisoformat(row["expires_at"])
    if datetime.datetime.utcnow() > expires_at:
        delete_session(token)
        return None
    return row

def delete_session(token: str):
    supabase.table("sessions").delete().eq("token", token).execute()
    st.session_state.pop("session_token", None)
    st.session_state.pop("user_id", None)

def restore_session():
    """Restaure la dernière session valide si elle existe"""
    if "session_token" in st.session_state:
        return
    resp = supabase.table("sessions").select("*").order("created_at", desc=True).execute()
    rows = resp.data
    for row in rows:
        expires_at = datetime.datetime.fromisoformat(row["expires_at"])
        if datetime.datetime.utcnow() < expires_at:
            st.session_state["session_token"] = row["token"]
            st.session_state["user_id"] = row["user_id"]
            break

def require_login():
    restore_session()
    token = st.session_state.get("session_token")
    if not token or not get_session(token):
        st.warning("Tu dois te connecter pour accéder à cette page.")
        st.stop()

# -------------------------
# Formulaire Streamlit
# -------------------------
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
                    st.experimental_rerun()
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
                        st.experimental_rerun()
                    else:
                        st.error("Erreur lors de la création du compte.")
