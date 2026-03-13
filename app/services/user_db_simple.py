import psycopg2
import os
import uuid

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

def create_user_table():
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            );
        """)
        conn.commit()

def add_user(email, password):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO users (email, password)
            VALUES (%s, %s)
            RETURNING id;
            """,
            (email, password),
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id

def create_user_convtable():
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id UUID PRIMARY KEY,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_conversations_user_id
            ON conversations(user_id);
        """)
        conn.commit()


def add_conversation(user_id, conversation_id=None):
    if conversation_id is None:
        conversation_id = str(uuid.uuid4())

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO conversations (id, user_id)
            VALUES (%s, %s)
            ON CONFLICT (id) DO NOTHING
            RETURNING id;
            """,
            (conversation_id, user_id),
        )
        result = cur.fetchone()

    conn.commit()
    return str(result[0]) if result else str(conversation_id)


def get_user_conversations(user_id):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, created_at
            FROM conversations
            WHERE user_id = %s
            ORDER BY created_at DESC;
            """,
            (user_id,),
        )
        rows = cur.fetchall()

    return [
        {
            "id": str(row[0]),
            "created_at": row[1].isoformat() if row[1] is not None else None,
        }
        for row in rows
    ]

def verify_user(email, password):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id
            FROM users
            WHERE email = %s AND password = %s;
            """,
            (email, password),
        )
        result = cur.fetchone()

    return result[0] if result else None

def init_user_conversation_schema():
    create_user_table()
    create_user_convtable()