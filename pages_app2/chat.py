import streamlit as st
from openai import OpenAI
from utils.db import (
    get_user_sessions,
    create_session,
    update_session_title,
    load_session_messages,
    save_message,
    clear_user_history,
)

user_id = st.session_state.get("user_id", "guest")
api_key = st.session_state.get("openai_api_key", "")

# 1. API Key 등록 여부 확인
if not api_key:
    st.title("💬 OpenAI AI 챗봇")
    st.warning("⚠️ **OpenAI API Key가 등록되지 않았습니다.**")
    st.info("좌측 사이드바의 **[🔑 API Key 등록]** 메뉴로 이동하여 먼저 API 키를 등록해주세요. (Key는 DB에 저장되지 않습니다)")
    st.stop()

# 2. 세션 상태 초기화 (현재 세션 확인)
user_sessions = get_user_sessions(user_id)

if "current_session_id" not in st.session_state or not st.session_state.current_session_id:
    if user_sessions:
        st.session_state.current_session_id = user_sessions[0][0]
    else:
        st.session_state.current_session_id = create_session(user_id, "새 대화")
        user_sessions = get_user_sessions(user_id)

# 3. 사이드바: 모델 설정 및 세션 관리
with st.sidebar:
    st.header("⚙️ 챗봇 설정")

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

    # 대화 세션 관리 (최대 10개 세션 보관)
    st.subheader("📂 대화 세션 (최대 10개)")
    st.caption("새 대화가 10개를 초과하면 가장 오래된 세션부터 자동 삭제됩니다.")

    if st.button("➕ 새 대화 시작", use_container_width=True):
        new_sid = create_session(user_id, "새 대화")
        st.session_state.current_session_id = new_sid
        st.rerun()

    if user_sessions:
        session_ids = [s[0] for s in user_sessions]
        session_labels = {s[0]: f"{s[1]} ({s[3]}개)" for s in user_sessions}

        curr_idx = session_ids.index(st.session_state.current_session_id) if st.session_state.current_session_id in session_ids else 0

        chosen_session = st.selectbox(
            "대화 세션 선택",
            options=session_ids,
            index=curr_idx,
            format_func=lambda sid: session_labels[sid],
        )

        if chosen_session != st.session_state.current_session_id:
            st.session_state.current_session_id = chosen_session
            st.rerun()

    st.divider()
    if st.button("내 모든 대화 내역 삭제", use_container_width=True):
        clear_user_history(user_id)
        new_sid = create_session(user_id, "새 대화")
        st.session_state.current_session_id = new_sid
        st.rerun()

# 4. 메인 화면: 대화 내역 출력
st.title("💬 OpenAI AI 챗봇")
st.caption(f"사용자: **{user_id}** | 적용 모델: **{selected_model}** (세션당 최대 100회 대화 보관)")

current_messages = load_session_messages(st.session_state.current_session_id)

for msg in current_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. 순수 텍스트 채팅 입력창
user_prompt = st.chat_input("메시지를 입력하세요...")

if user_prompt:
    # 첫 메시지일 경우 세션 제목 자동 갱신
    if len(current_messages) == 0:
        update_session_title(st.session_state.current_session_id, user_prompt)

    # 사용자 메시지 DB 저장 (FIFO 자동 적용)
    save_message(st.session_state.current_session_id, "user", user_prompt)

    # 화면에 사용자 메시지 출력
    with st.chat_message("user"):
        st.write(user_prompt)

    # OpenAI API 호출 (gpt-5.6-luna 기본)
    client = OpenAI(api_key=api_key)

    # 이전 대화 맥락 구성
    history = load_session_messages(st.session_state.current_session_id)
    api_messages = [{"role": h["role"], "content": h["content"]} for h in history]

    # 실시간 스트리밍 답변 렌더링
    stream = client.chat.completions.create(
        model=selected_model,
        messages=api_messages,
        stream=True,
    )

    with st.chat_message("assistant"):
        response_text = st.write_stream(stream)

    # 어시스턴트 메시지 DB 저장 (FIFO 자동 적용)
    save_message(st.session_state.current_session_id, "assistant", response_text)
    st.rerun()
