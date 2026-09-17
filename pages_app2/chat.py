import streamlit as st
from openai import OpenAI
from utils.db import (
    get_user_sessions,
    create_session,
    update_session_title,
    load_session_messages,
    save_message,
    delete_session,
    clear_user_history,
)
from utils.ui_theme import apply_custom_theme

apply_custom_theme()

user_id = st.session_state.get("user_id", "guest")
api_key = st.session_state.get("openai_api_key", "")

# 1. API Key 등록 확인
if not api_key:
    st.title("💬 채팅")
    st.warning("OpenAI API Key가 등록되지 않았습니다.")
    st.info("좌측 메뉴의 **[API Key 등록]** 페이지에서 먼저 Key를 등록해주세요.")
    st.stop()

# 2. 세션 초기화
user_sessions = get_user_sessions(user_id)

if "current_session_id" not in st.session_state or not st.session_state.current_session_id:
    if user_sessions:
        st.session_state.current_session_id = user_sessions[0][0]
    else:
        st.session_state.current_session_id = create_session(user_id, "새 대화")
        user_sessions = get_user_sessions(user_id)

current_sid = st.session_state.current_session_id
current_session_info = next((s for s in user_sessions if s[0] == current_sid), None)
current_title = current_session_info[1] if current_session_info else "대화"

# 3. 사이드바: 새 대화, 모델 선택, 세션 선택
with st.sidebar:
    if st.button("➕ 새 대화", use_container_width=True, type="primary"):
        new_sid = create_session(user_id, "새 대화")
        st.session_state.current_session_id = new_sid
        st.rerun()

    # 모델 선택 (기본값: gpt-5.6-luna)
    model_options = [
        "gpt-5.6-luna",
        "gpt-5.6-terra",
        "gpt-5.6-sol",
        "gpt-5.5",
        "gpt-6-astra",
    ]
    selected_model = st.selectbox("모델 선택", options=model_options, index=0)

    st.divider()

    # 세션 목록
    if user_sessions:
        session_ids = [s[0] for s in user_sessions]
        session_labels = {s[0]: s[1] for s in user_sessions}
        curr_idx = session_ids.index(current_sid) if current_sid in session_ids else 0

        chosen_session = st.selectbox(
            "대화 목록",
            options=session_ids,
            index=curr_idx,
            format_func=lambda sid: session_labels[sid],
        )
        if chosen_session != current_sid:
            st.session_state.current_session_id = chosen_session
            st.rerun()

    st.divider()

    if st.button("현재 대화 삭제", use_container_width=True):
        delete_session(current_sid)
        st.session_state.pop("current_session_id", None)
        st.rerun()

    if st.button("모든 대화 초기화", use_container_width=True):
        clear_user_history(user_id)
        new_sid = create_session(user_id, "새 대화")
        st.session_state.current_session_id = new_sid
        st.rerun()

# 4. 메인 화면
st.title(f"💬 {current_title}")

current_messages = load_session_messages(current_sid)

for msg in current_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. 채팅 입력
user_prompt = st.chat_input("메시지를 입력하세요...")

if user_prompt:
    if len(current_messages) == 0 and current_title == "새 대화":
        update_session_title(current_sid, user_prompt)

    save_message(current_sid, "user", user_prompt)

    with st.chat_message("user"):
        st.write(user_prompt)

    client = OpenAI(api_key=api_key)
    history = load_session_messages(current_sid)
    api_messages = [{"role": h["role"], "content": h["content"]} for h in history]

    stream = client.chat.completions.create(
        model=selected_model,
        messages=api_messages,
        stream=True,
    )

    with st.chat_message("assistant"):
        response_text = st.write_stream(stream)

    save_message(current_sid, "assistant", response_text)
    st.rerun()
