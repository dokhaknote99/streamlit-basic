import base64
import datetime
import os
import sqlite3
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# 1. .env 환경변수 로드
load_dotenv()

# ==================================================
# SQLite 데이터베이스 세션 및 메시지 관리
# ==================================================
DB_FILE = "chat_history.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            file_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(messages)")
    cols = [c[1] for c in cursor.fetchall()]
    if "session_id" not in cols:
        conn.execute("ALTER TABLE messages ADD COLUMN session_id TEXT DEFAULT 'default_session'")
    conn.commit()
    conn.close()

def get_all_sessions():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, created_at FROM sessions ORDER BY created_at DESC")
    sessions = cursor.fetchall()
    conn.close()
    return sessions

def create_session(title="새 대화"):
    session_id = "session_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    conn = sqlite3.connect(DB_FILE)
    conn.execute("INSERT INTO sessions (id, title) VALUES (?, ?)", (session_id, title))
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
        "SELECT role, content, file_name FROM messages WHERE session_id = ? ORDER BY id ASC",
        (session_id,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1], "file_name": r[2]} for r in rows]

def save_message(session_id, role, content, file_name=None):
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT INTO messages (session_id, role, content, file_name) VALUES (?, ?, ?, ?)",
        (session_id, role, content, file_name),
    )
    conn.commit()
    conn.close()

def clear_all_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("DELETE FROM messages")
    conn.execute("DELETE FROM sessions")
    conn.commit()
    conn.close()

# DB 초기화
init_db()

# 세션 상태 초기화
if "current_session_id" not in st.session_state:
    sessions = get_all_sessions()
    if sessions:
        st.session_state.current_session_id = sessions[0][0]
    else:
        st.session_state.current_session_id = create_session("첫 번째 대화")

if "staged_image" not in st.session_state:
    st.session_state.staged_image = None

if "staged_file" not in st.session_state:
    st.session_state.staged_file = None

# ==================================================
# 팝업 다이얼로그 (이미지 및 파일 업로드)
# ==================================================
@st.dialog("🖼️ 이미지 첨부 (드래그 앤 드롭)")
def open_image_upload_dialog():
    st.write("아래 상자에 이미지를 드래그 앤 드롭하거나 클릭하여 파일을 선택하세요.")
    uploaded_img = st.file_uploader(
        "이미지 파일 선택",
        type=["png", "jpg", "jpeg", "webp", "gif"],
    )
    if uploaded_img:
        st.image(uploaded_img, width=280, caption=f"선택된 이미지: {uploaded_img.name}")
        if st.button("이 이미지 첨부하기", use_container_width=True):
            st.session_state.staged_image = {
                "name": uploaded_img.name,
                "bytes": uploaded_img.read(),
                "type": uploaded_img.type,
            }
            st.rerun()

@st.dialog("📁 문서/코드 파일 첨부 (드래그 앤 드롭)")
def open_file_upload_dialog():
    st.write("텍스트, 코드, CSV 등의 문서 파일을 드래그 앤 드롭하세요.")
    uploaded_doc = st.file_uploader(
        "문서 파일 선택",
        type=["txt", "py", "csv", "md", "json", "html"],
    )
    if uploaded_doc:
        st.write(f"📄 파일명: **{uploaded_doc.name}** ({uploaded_doc.size:,} bytes)")
        if st.button("이 파일 첨부하기", use_container_width=True):
            st.session_state.staged_file = {
                "name": uploaded_doc.name,
                "bytes": uploaded_doc.read(),
            }
            st.rerun()

# ==================================================
# 사이드바: 대화 관리 및 모델 설정
# ==================================================
with st.sidebar:
    st.header("⚙️ 챗봇 설정")
    api_key = os.environ.get("OPENAI_API_KEY", "")
    st.text_input("OpenAI API Key (.env)", value="●●●●●●●●" if api_key else "키 없음", disabled=True)

    # 모델 선택 (기본값: gpt-5.6-luna)
    model_options = [
        "gpt-5.6-luna",
        "gpt-5.6-terra",
        "gpt-5.6-sol",
        "gpt-5.5",
        "gpt-6-astra",
    ]
    selected_model = st.selectbox(
        label="🤖 모델 선택 (GPT 5.5+)",
        options=model_options,
        index=0,
    )

    st.divider()

    # 대화 세션 관리
    st.subheader("📂 대화 세션 관리")

    if st.button("➕ 새 대화 시작", use_container_width=True):
        new_sid = create_session("새 대화")
        st.session_state.current_session_id = new_sid
        st.session_state.staged_image = None
        st.session_state.staged_file = None
        st.rerun()

    all_sessions = get_all_sessions()
    if all_sessions:
        session_ids = [s[0] for s in all_sessions]
        session_labels = {s[0]: f"{s[1]} ({s[2][:16]})" for s in all_sessions}

        curr_idx = session_ids.index(st.session_state.current_session_id) if st.session_state.current_session_id in session_ids else 0

        chosen_session = st.selectbox(
            "대화 선택",
            options=session_ids,
            index=curr_idx,
            format_func=lambda sid: session_labels[sid],
        )

        if chosen_session != st.session_state.current_session_id:
            st.session_state.current_session_id = chosen_session
            st.rerun()

    st.divider()
    if st.button("전체 대화 내역 초기화 (DB 삭제)", use_container_width=True):
        clear_all_db()
        new_sid = create_session("새 대화")
        st.session_state.current_session_id = new_sid
        st.rerun()

# ==================================================
# 메인 화면: 대화 내역 및 입력창
# ==================================================
st.title("💬 OpenAI AI 챗봇")
st.caption(f"현재 대화 세션: **{st.session_state.current_session_id}** | 적용 모델: **{selected_model}**")

# 현재 세션의 메시지 로드 및 출력
current_messages = load_session_messages(st.session_state.current_session_id)

for msg in current_messages:
    with st.chat_message(msg["role"]):
        if msg.get("file_name"):
            st.caption(f"📎 첨부파일: {msg['file_name']}")
        st.write(msg["content"])

# --------------------------------------------------
# 업로드 버튼 분리 및 첨부 상태 바
# --------------------------------------------------
btn_col1, btn_col2, status_col = st.columns([1.5, 1.5, 5], vertical_alignment="center")

with btn_col1:
    if st.button("🖼️ 이미지 업로드", use_container_width=True):
        open_image_upload_dialog()

with btn_col2:
    if st.button("📁 파일 업로드", use_container_width=True):
        open_file_upload_dialog()

with status_col:
    # 첨부 대기 상태 표시
    staged_items = []
    if st.session_state.staged_image:
        staged_items.append(f"🖼️ {st.session_state.staged_image['name']}")
    if st.session_state.staged_file:
        staged_items.append(f"📁 {st.session_state.staged_file['name']}")

    if staged_items:
        st.info("첨부 대기 중: " + ", ".join(staged_items))
        if st.button("❌ 첨부 취소"):
            st.session_state.staged_image = None
            st.session_state.staged_file = None
            st.rerun()

# --------------------------------------------------
# 채팅 메시지 입력 및 전송
# --------------------------------------------------
user_prompt = st.chat_input("메시지를 입력하세요...")

if user_prompt:
    attached_names = []
    api_content = []
    final_prompt = user_prompt

    # 1. 첨부된 이미지 처리
    if st.session_state.staged_image:
        img_info = st.session_state.staged_image
        b64_data = base64.b64encode(img_info["bytes"]).decode("utf-8")
        api_content.append({
            "type": "image_url",
            "image_url": {"url": f"data:{img_info['type']};base64,{b64_data}"},
        })
        attached_names.append(img_info["name"])

    # 2. 첨부된 텍스트/문서 파일 처리
    if st.session_state.staged_file:
        file_info = st.session_state.staged_file
        doc_text = file_info["bytes"].decode("utf-8", errors="replace")
        final_prompt += f"\n\n[첨부파일 ({file_info['name']}) 내용]:\n{doc_text}"
        attached_names.append(file_info["name"])

    api_content.insert(0, {"type": "text", "text": final_prompt})
    file_label = ", ".join(attached_names) if attached_names else None

    # 첫 메시지일 경우 세션 제목 자동 갱신
    if len(current_messages) == 0:
        update_session_title(st.session_state.current_session_id, user_prompt)

    # SQLite DB에 사용자 메시지 저장
    save_message(st.session_state.current_session_id, "user", final_prompt, file_label)

    # 화면에 사용자 메시지 출력
    with st.chat_message("user"):
        if file_label:
            st.caption(f"📎 첨부: {file_label}")
        if st.session_state.staged_image:
            st.image(st.session_state.staged_image["bytes"], width=300)
        st.write(user_prompt)

    # 첨부 상태 초기화
    st.session_state.staged_image = None
    st.session_state.staged_file = None

    # 3. OpenAI API 스트리밍 호출
    client = OpenAI(api_key=api_key)

    history = load_session_messages(st.session_state.current_session_id)
    api_messages = []
    for h in history[:-1]:
        api_messages.append({"role": h["role"], "content": h["content"]})

    latest_content = api_content if any(c.get("type") == "image_url" for c in api_content) else final_prompt
    api_messages.append({"role": "user", "content": latest_content})

    stream = client.chat.completions.create(
        model=selected_model,
        messages=api_messages,
        stream=True,
    )

    with st.chat_message("assistant"):
        response_text = st.write_stream(stream)

    # SQLite DB에 어시스턴트 메시지 저장
    save_message(st.session_state.current_session_id, "assistant", response_text)
    st.rerun()

