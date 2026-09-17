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

# 1. API Key 등록 검증
if not api_key:
    st.title("💬 채팅")
    st.warning("OpenAI API Key가 등록되지 않았습니다.")
    if st.button("🔑 API Key 등록하러 가기", type="primary"):
        st.switch_page("pages_app2/key_settings.py")
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

# 3. 사이드바: 채팅 전용 옵션
with st.sidebar:
    st.subheader("💬 채팅 옵션")

    if st.button("➕ 새 대화 시작", use_container_width=True, type="primary"):
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
    selected_model = st.selectbox("언어 모델 선택", options=model_options, index=0)

    st.divider()

    # 대화 세션 목록
    if user_sessions:
        session_ids = [s[0] for s in user_sessions]
        session_labels = {s[0]: s[1] for s in user_sessions}
        curr_idx = session_ids.index(current_sid) if current_sid in session_ids else 0

        chosen_session = st.selectbox(
            "대화 세션 선택",
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

# 4. 상단 헤더
col_head, col_meta = st.columns([3, 1])
with col_head:
    st.title(f"💬 {current_title}")
with col_meta:
    st.caption(f"적용 모델: **{selected_model}**")

# 5. 스크롤 가능한 전용 채팅 뷰포트 컨테이너 (고정 높이로 안정적인 레이아웃)
current_messages = load_session_messages(current_sid)
chat_container = st.container(height=520, border=True)

with chat_container:
    if len(current_messages) == 0:
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        _, empty_col, _ = st.columns([1, 1.2, 1])
        with empty_col:
            st.image("assets/logo.jpg", width=72)
            st.subheader("새로운 대화를 시작해보세요!")
            st.caption("궁금한 점이나 작성할 코드, 아이디어를 아래 입력창에 입력해주세요.")
    else:
        for msg in current_messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

# 6. 채팅창 바로 아래 전용 입력창 도킹
user_prompt = st.chat_input("메시지를 입력하세요... (Enter 키로 전송)")

if user_prompt:
    if len(current_messages) == 0 and current_title == "새 대화":
        update_session_title(current_sid, user_prompt)

    save_message(current_sid, "user", user_prompt)

    with chat_container:
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

    with chat_container:
        with st.chat_message("assistant"):
            response_text = st.write_stream(stream)

    save_message(current_sid, "assistant", response_text)
    st.rerun()
