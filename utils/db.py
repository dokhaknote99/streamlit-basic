import datetime
import sqlite3

DB_FILE = "chat_history.db"
MAX_SESSIONS_PER_USER = 10
MAX_MESSAGES_PER_SESSION = 200  # 내채팅 + AI답변 = 1회(2개 레코드), 100회 = 200개

def init_db():
    conn = sqlite3.connect(DB_FILE)
    # 1. 세션 테이블 (user_id 포함, API Key 컬럼 없음)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # 2. 메시지 테이블 (API Key 컬럼 없음)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 기존 DB 마이그레이션 호환 (user_id 컬럼 여부 확인)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(sessions)")
    s_cols = [c[1] for c in cursor.fetchall()]
    if "user_id" not in s_cols:
        conn.execute("ALTER TABLE sessions ADD COLUMN user_id TEXT DEFAULT 'guest'")

    conn.commit()
    conn.close()

def get_user_sessions(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT s.id, s.title, s.created_at, COUNT(m.id) as msg_count
        FROM sessions s
        LEFT JOIN messages m ON s.id = m.session_id
        WHERE s.user_id = ?
        GROUP BY s.id
        ORDER BY s.created_at DESC
        """,
        (user_id,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

def create_session(user_id, title="새 대화"):
    session_id = f"session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT INTO sessions (id, user_id, title) VALUES (?, ?, ?)",
        (session_id, user_id, title),
    )
    conn.commit()

    # FIFO 정책: 유저당 최대 10개 세션 유지 (오래된 세션 자동 삭제)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM sessions WHERE user_id = ? ORDER BY created_at ASC", (user_id,))
    user_sessions = cursor.fetchall()

    if len(user_sessions) > MAX_SESSIONS_PER_USER:
        delete_count = len(user_sessions) - MAX_SESSIONS_PER_USER
        old_sessions_to_delete = [row[0] for row in user_sessions[:delete_count]]
        for old_sid in old_sessions_to_delete:
            conn.execute("DELETE FROM messages WHERE session_id = ?", (old_sid,))
            conn.execute("DELETE FROM sessions WHERE id = ?", (old_sid,))
        conn.commit()

    conn.close()
    return session_id

def update_session_title(session_id, title):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("UPDATE sessions SET title = ? WHERE id = ?", (title[:30], session_id))
    conn.commit()
    conn.close()

def load_session_messages(session_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content, created_at FROM messages WHERE session_id = ? ORDER BY id ASC",
        (session_id,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1], "created_at": r[2]} for r in rows]

def save_message(session_id, role, content):
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, content),
    )
    conn.commit()

    # FIFO 정책: 세션당 최대 100회 대화(200개 메시지) 유지 (오래된 메시지 자동 삭제)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM messages WHERE session_id = ? ORDER BY id ASC", (session_id,))
    msg_ids = cursor.fetchall()

    if len(msg_ids) > MAX_MESSAGES_PER_SESSION:
        delete_count = len(msg_ids) - MAX_MESSAGES_PER_SESSION
        ids_to_delete = [row[0] for row in msg_ids[:delete_count]]
        cursor.executemany("DELETE FROM messages WHERE id = ?", [(mid,) for mid in ids_to_delete])
        conn.commit()

    conn.close()

def delete_session(session_id):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()

def clear_user_history(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM sessions WHERE user_id = ?", (user_id,))
    sids = [row[0] for row in cursor.fetchall()]
    for sid in sids:
        conn.execute("DELETE FROM messages WHERE session_id = ?", (sid,))
    conn.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
