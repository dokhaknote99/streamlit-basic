import streamlit as st
from utils.ui_theme import apply_custom_theme

apply_custom_theme()

current_user = st.session_state.get("user_id")

if not current_user:
    st.title("👤 사용자 로그인")
    col_intro, col_form = st.columns([1, 1], gap="large")

    with col_intro:
        st.image("assets/auth_hero.jpg", width="stretch")
        st.caption("AI Assistant와 함께 개인화된 대화 세션과 스마트한 작업을 경험해보세요.")

    with col_form:
        with st.container(border=True):
            st.subheader("계정 접속")
            username_input = st.text_input(
                "사용자 ID",
                placeholder="아이디 또는 닉네임을 입력하세요",
            )
            if st.button("로그인", use_container_width=True, type="primary"):
                if username_input.strip():
                    st.session_state["user_id"] = username_input.strip()
                    st.rerun()
                else:
                    st.warning("사용자 ID를 입력해주세요.")

else:
    st.title(f"👤 계정 관리 ({current_user})")
    col_info, col_nav = st.columns([1, 1], gap="large")

    with col_info:
        st.image("assets/auth_hero.jpg", width="stretch")
        with st.container(border=True):
            st.subheader("접속 상태")
            st.write(f"로그인 계정: **{current_user}**")
            has_key = bool(st.session_state.get("openai_api_key"))
            st.write(f"API Key: **{'등록됨 ✅' if has_key else '미등록 ⚠️'}**")

            if st.button("🚪 로그아웃", use_container_width=True):
                st.session_state.pop("user_id", None)
                st.session_state.pop("openai_api_key", None)
                st.session_state.pop("current_session_id", None)
                st.rerun()

    with col_nav:
        with st.container(border=True):
            st.subheader("바로가기")
            if st.button("💬 채팅하러 가기", use_container_width=True, type="primary"):
                st.switch_page("pages_app2/chat.py")
            if st.button("🔑 API Key 관리", use_container_width=True):
                st.switch_page("pages_app2/key_settings.py")
            if st.button("📜 대화 내역 조회", use_container_width=True):
                st.switch_page("pages_app2/history.py")
