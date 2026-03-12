import sqlite3
import uuid
from datetime import datetime, timedelta

DB_PATH = "data/auth_system.db"

def init_auth_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table des utilisateurs
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE
    )''')
    
    # Table des sessions (le lien entre le cookie et l'utilisateur)
    cursor.execute('''CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        user_id TEXT,
        expires_at TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    conn.commit()
    conn.close()

def get_or_create_user(email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    
    if user:
        user_id = user[0]
    else:
        user_id = str(uuid.uuid4())
        cursor.execute("INSERT INTO users (id, email) VALUES (?, ?)", (user_id, email))
        conn.commit()
    
    conn.close()
    return user_id

def create_session(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    session_id = str(uuid.uuid4())
    # Session valide 30 jours
    expires_at = datetime.now() + timedelta(days=30)
    cursor.execute("INSERT INTO sessions (session_id, user_id, expires_at) VALUES (?, ?, ?)", 
                   (session_id, user_id, expires_at))
    conn.commit()
    conn.close()
    return session_id

def verify_session(session_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM sessions WHERE session_id = ? AND expires_at > ?", 
                   (session_id, datetime.now()))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
