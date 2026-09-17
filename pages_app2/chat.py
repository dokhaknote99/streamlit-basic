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
from utils.ui_theme import apply_custom_theme, page_header, empty_state, session_labels

apply_custom_theme()

ASSISTANT_AVATAR = "assets/logo.jpg"

user_id = st.session_state.get("user_id", "guest")
api_key = st.session_state.get("openai_api_key", "")

# 1. API Key 등록 검증
if not api_key:
    page_header("💬", "채팅", "대화를 시작하려면 먼저 OpenAI API Key를 등록해주세요.")
    _, col_center, _ = st.columns([1, 1.3, 1])
    with col_center:
        with st.container(border=True, key="card_no_key"):
            empty_state(
                "API Key가 아직 없어요",
                "OpenAI API Key를 등록하면 바로 대화를 시작할 수 있습니다. 키는 브라우저 세션에만 보관됩니다.",
            )
            if st.button("🔑 API Key 등록하러 가기", type="primary", width="stretch"):
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
    if st.button("새 대화", icon=":material/add:", width="stretch", type="primary"):
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
    selected_model = st.selectbox("모델", options=model_options, index=0)

    st.divider()

    # 대화 세션 목록 (리스트 형태로 스타일링된 라디오)
    if user_sessions:
        st.caption("대화 목록")
        session_ids = [s[0] for s in user_sessions]
        label_map = session_labels(user_sessions)

        def _on_pick_session():
            st.session_state.current_session_id = st.session_state["session_list_chat"]

        # 새 대화/삭제 등으로 현재 세션이 바뀐 경우 위젯 선택값을 동기화
        if st.session_state.get("session_list_chat") != current_sid:
            st.session_state["session_list_chat"] = current_sid

        st.radio(
            "대화 세션 선택",
            options=session_ids,
            format_func=lambda sid: label_map[sid],
            label_visibility="collapsed",
            width="stretch",
            key="session_list_chat",
            on_change=_on_pick_session,
        )

    st.divider()

    with st.expander("대화 관리", icon=":material/settings:"):
        if st.button("현재 대화 삭제", icon=":material/delete:", width="stretch"):
            delete_session(current_sid)
            st.session_state.pop("current_session_id", None)
            st.rerun()

        if st.button("모든 대화 초기화", icon=":material/delete_sweep:", width="stretch"):
            clear_user_history(user_id)
            new_sid = create_session(user_id, "새 대화")
            st.session_state.current_session_id = new_sid
            st.rerun()

# 4. 상단 헤더
current_messages = load_session_messages(current_sid)
page_header(
    "💬",
    current_title,
    chips=[(selected_model, ""), (f"메시지 {len(current_messages)}개", "gray")],
)

# 5. 스크롤 가능한 전용 채팅 뷰포트 컨테이너 (고정 높이로 안정적인 레이아웃)
chat_container = st.container(height=540, border=True, key="card_chat")

with chat_container:
    if len(current_messages) == 0:
        # 첫 메시지 전송 시 비울 수 있도록 placeholder에 렌더링
        empty_slot = st.empty()
        with empty_slot.container():
            empty_state(
                "새로운 대화를 시작해보세요!",
                "궁금한 점, 작성할 코드, 떠오른 아이디어를 아래 입력창에 적어주세요.",
            )
    else:
        for msg in current_messages:
            avatar = ASSISTANT_AVATAR if msg["role"] == "assistant" else None
            with st.chat_message(msg["role"], avatar=avatar):
                st.write(msg["content"])

# 6. 채팅창 바로 아래 전용 입력창 도킹
user_prompt = st.chat_input("메시지를 입력하세요... (Enter 키로 전송)")

if user_prompt:
    if len(current_messages) == 0:
        empty_slot.empty()
        if current_title == "새 대화":
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
        with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
            response_text = st.write_stream(stream)

    save_message(current_sid, "assistant", response_text)
    st.rerun()
