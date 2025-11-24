# utils/auth_duckdb_form.py
import datetime
import hashlib
import os
import secrets
from pathlib import Path

import duckdb

import streamlit as st

# --- Paramètres ---
DB_PATH = Path(__file__).resolve().parents[1] / "data" / "app.db"
PBKDF2_ITER = 200_000
HASH_NAME = "sha256"
SALT_BYTES = 16
TOKEN_BYTES = 32
SESSION_DURATION_HOURS = 24 * 7  # 7 jours


# --- Connexion à la base de données ---
@st.cache_resource
def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(database=str(DB_PATH), read_only=False)


# --- Initialisation des tables ---
def init_db():
    conn = get_conn()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE,
            username TEXT,
            password_hash TEXT,
            salt TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    """
    )


# --- Hachage et gestion utilisateur ---
def _hash_password(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac(HASH_NAME, password.encode(), salt, PBKDF2_ITER).hex()


def create_user(email: str, username: str, password: str):
    conn = get_conn()
    max_id = conn.execute("SELECT MAX(id) FROM users").fetchone()[0] or 0
    salt = os.urandom(SALT_BYTES)
    password_hash = _hash_password(password, salt)
    try:
        conn.execute(
            "INSERT INTO users (id, email, username, password_hash, salt) VALUES (?, ?, ?, ?, ?)",
            [max_id + 1, email.lower(), username, password_hash, salt.hex()],
        )
        row = conn.execute(
            "SELECT id, email, username FROM users WHERE email = ?", [email.lower()]
        ).fetchone()
        return {"id": row[0], "email": row[1], "username": row[2]} if row else None
    except duckdb.DuckDBException:
        return None


def get_user_by_email(email: str):
    conn = get_conn()
    row = conn.execute(
        "SELECT id, email, username, password_hash, salt, created_at FROM users WHERE email = ?",
        [email.lower()],
    ).fetchone()
    if row:
        return dict(
            zip(["id", "email", "username", "password_hash", "salt", "created_at"], row)
        )
    return None


def verify_password(stored_hash: str, salt_hex: str, password: str) -> bool:
    return secrets.compare_digest(
        _hash_password(password, bytes.fromhex(salt_hex)), stored_hash
    )


def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    return (
        {"id": user["id"], "email": user["email"], "username": user["username"]}
        if user and verify_password(user["password_hash"], user["salt"], password)
        else None
    )


# --- Gestion des sessions ---
def create_session(user_id: int):
    token = secrets.token_urlsafe(TOKEN_BYTES)
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(
        hours=SESSION_DURATION_HOURS
    )
    conn = get_conn()
    conn.execute(
        "INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)",
        [token, user_id, expires_at],
    )
    st.session_state["session_token"] = token
    st.session_state["user_id"] = user_id
    return token


def get_session(token: str):
    conn = get_conn()
    row = conn.execute(
        "SELECT token, user_id, created_at, expires_at FROM sessions WHERE token = ?",
        [token],
    ).fetchone()
    if not row:
        return None
    expires_at = row[3]
    if isinstance(expires_at, str):
        expires_at = datetime.datetime.fromisoformat(expires_at)
    if datetime.datetime.utcnow() > expires_at:
        delete_session(token)
        return None
    return dict(zip(["token", "user_id", "created_at", "expires_at"], row))


def delete_session(token: str):
    if not token:
        return
    conn = get_conn()
    conn.execute("DELETE FROM sessions WHERE token = ?", [token])
    st.session_state.pop("session_token", None)
    st.session_state.pop("user_id", None)


def restore_session():
    if "session_token" not in st.session_state:
        conn = get_conn()
        row = conn.execute(
            """
            SELECT token, user_id, expires_at
            FROM sessions
            WHERE expires_at > CURRENT_TIMESTAMP
            ORDER BY created_at DESC LIMIT 1
        """
        ).fetchone()
        if row:
            st.session_state["session_token"] = row[0]
            st.session_state["user_id"] = row[1]


def require_login():
    restore_session()
    token = st.session_state.get("session_token")
    if not token or not get_session(token):
        st.warning("Tu dois te connecter pour accéder à cette page.")
        st.stop()


# --- Formulaire Streamlit avec st.form ---
def auth_form():
    init_db()
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
