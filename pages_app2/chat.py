import streamlit as st
from openai import OpenAI
from utils.db import (
    get_user_sessions,
    create_session,
    update_session_title,
    load_session_messages,
    save_message,
    clear_user_history,
    delete_session,
)
from utils.ui_theme import apply_custom_theme

apply_custom_theme()

user_id = st.session_state.get("user_id", "guest")
api_key = st.session_state.get("openai_api_key", "")

# 1. API Key 등록 여부 검증
if not api_key:
    st.markdown(
        """
        <div style="background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 14px; padding: 24px; text-align: center; margin-top: 40px;">
            <div style="font-size: 2.5rem; margin-bottom: 8px;">⚠️</div>
            <h2 style="font-size: 1.4rem; font-weight: 700; margin-bottom: 8px;">OpenAI API Key가 등록되지 않았습니다</h2>
            <p style="color: gray; font-size: 0.95rem; margin-bottom: 20px;">
                챗봇과 실시간 대화를 나누려면 먼저 개인 API Key를 등록해야 합니다.<br>
                입력하신 Key는 데이터베이스에 저장되지 않고 현재 브라우저 메모리에만 안전하게 보관됩니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([1, 1, 1])
    with btn_col:
        if st.button("🔑 지금 API Key 등록하러 가기", use_container_width=True, type="primary"):
            st.switch_page("pages_app2/key_settings.py")
    st.stop()

# 2. 대화 세션 상태 초기화
user_sessions = get_user_sessions(user_id)

if "current_session_id" not in st.session_state or not st.session_state.current_session_id:
    if user_sessions:
        st.session_state.current_session_id = user_sessions[0][0]
    else:
        st.session_state.current_session_id = create_session(user_id, "새 대화")
        user_sessions = get_user_sessions(user_id)

current_sid = st.session_state.current_session_id
current_session_info = next((s for s in user_sessions if s[0] == current_sid), None)
current_title = current_session_info[1] if current_session_info else "대화방"

# 3. 사이드바: 모델 설정 및 세션 네비게이션
with st.sidebar:
    st.markdown("### ⚙️ 모델 및 대화 설정")

    # OpenAI 차세대 모델 선택 (기본값: gpt-5.6-luna)
    model_options = [
        "gpt-5.6-luna",
        "gpt-5.6-terra",
        "gpt-5.6-sol",
        "gpt-5.5",
        "gpt-6-astra",
    ]
    selected_model = st.selectbox(
        label="🤖 언어 모델 (GPT 5.5+)",
        options=model_options,
        index=0,
        help="사용자 규칙에 따라 기본 모델로 gpt-5.6-luna가 지정되어 있습니다.",
    )
    st.caption(f"⚡ 선택된 모델: `{selected_model}`")

    st.divider()

    # 대화 세션 관리 (최대 10개)
    st.markdown("### 📂 내 대화 세션")
    
    # 세션 보관 용량 게이지
    session_count = len(user_sessions)
    st.caption(f"보관 세션: **{session_count} / 10개** (초과 시 FIFO 자동 삭제)")
    st.progress(min(session_count / 10.0, 1.0))

    if st.button("➕ 새 대화 시작", use_container_width=True, type="primary"):
        new_sid = create_session(user_id, "새 대화")
        st.session_state.current_session_id = new_sid
        st.rerun()

    if user_sessions:
        session_ids = [s[0] for s in user_sessions]
        session_labels = {s[0]: f"{s[1]} ({s[3]}건)" for s in user_sessions}

        curr_idx = session_ids.index(current_sid) if current_sid in session_ids else 0

        chosen_session = st.selectbox(
            "대화 세션 선택",
            options=session_ids,
            index=curr_idx,
            format_func=lambda sid: session_labels[sid],
            label_visibility="collapsed",
        )

        if chosen_session != current_sid:
            st.session_state.current_session_id = chosen_session
            st.rerun()

    st.divider()

    # 위험 구역 (전체 삭제)
    with st.expander("🚨 세션 관리 및 초기화", expanded=False):
        if st.button("🗑️ 현재 선택된 세션 삭제", use_container_width=True):
            delete_session(current_sid)
            st.session_state.pop("current_session_id", None)
            st.rerun()

        if st.button("⚠️ 내 모든 대화 내역 영구 삭제", use_container_width=True):
            clear_user_history(user_id)
            new_sid = create_session(user_id, "새 대화")
            st.session_state.current_session_id = new_sid
            st.rerun()

# 4. 메인 대화 화면 헤더
current_messages = load_session_messages(current_sid)
msg_count = len(current_messages)

header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
            <h2 style="margin: 0; font-size: 1.5rem; font-weight: 800;">💬 {current_title}</h2>
            <span class="status-chip status-info">🤖 {selected_model}</span>
            <span class="status-chip status-active">📊 {msg_count} / 200 msgs</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
with header_col2:
    with st.popover("✏️ 대화 제목 수정", use_container_width=True):
        new_title = st.text_input("새 대화 제목", value=current_title)
        if st.button("제목 저장", use_container_width=True):
            if new_title.strip():
                update_session_title(current_sid, new_title.strip())
                st.rerun()

st.divider()

# 5. 빈 대화 상태 온보딩 뷰 (추천 질문 칩)
prompt_to_trigger = None

if msg_count == 0:
    st.markdown(
        f"""
        <div style="text-align: center; padding: 24px 0 16px 0;">
            <div style="font-size: 2.2rem; margin-bottom: 6px;">👋</div>
            <h3 style="font-size: 1.4rem; font-weight: 700; margin-bottom: 4px;">반갑습니다, {user_id}님! 무엇을 도와드릴까요?</h3>
            <p style="color: gray; font-size: 0.95rem;">직접 질문을 입력하시거나 아래 추천 프롬프트를 클릭해보세요.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        if st.button(
            "💡 **Streamlit 노하우**\n\n'Streamlit에서 Session State를 효율적으로 관리하는 패턴 3가지 알려줘'",
            use_container_width=True,
        ):
            prompt_to_trigger = "Streamlit에서 Session State를 효율적으로 관리하는 패턴 3가지 알려줘"

    with sc2:
        if st.button(
            "🚀 **차세대 LLM 분석**\n\n'GPT-5.6-Luna의 주요 특징과 장점을 깔끔하게 요약해줘'",
            use_container_width=True,
        ):
            prompt_to_trigger = "GPT-5.6-Luna의 주요 특징과 장점을 깔끔하게 요약해줘"

    with sc3:
        if st.button(
            "📊 **데이터 엔지니어링**\n\n'Python으로 SQLite 대화 로그를 분석하고 시각화하는 방법 알려줘'",
            use_container_width=True,
        ):
            prompt_to_trigger = "Python으로 SQLite 대화 로그를 분석하고 시각화하는 방법 알려줘"

# 6. 기존 대화 메시지 렌더링
for msg in current_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. 순수 텍스트 채팅 입력창
user_input = st.chat_input("메시지를 입력하세요... (텍스트 대화 전용)")
final_prompt = prompt_to_trigger if prompt_to_trigger else user_input

if final_prompt:
    # 첫 메시지일 경우 세션 제목 자동 갱신
    if len(current_messages) == 0 and current_title == "새 대화":
        update_session_title(current_sid, final_prompt)

    # 사용자 메시지 DB 저장 (FIFO 자동 적용)
    save_message(current_sid, "user", final_prompt)

    # 화면에 사용자 메시지 출력
    with st.chat_message("user"):
        st.write(final_prompt)

    # OpenAI API 호출 (gpt-5.6-luna 기본)
    client = OpenAI(api_key=api_key)

    # 이전 대화 맥락 구성
    history = load_session_messages(current_sid)
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
    save_message(current_sid, "assistant", response_text)
    st.rerun()
