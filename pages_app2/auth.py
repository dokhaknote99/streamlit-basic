import streamlit as st
from utils.ui_theme import apply_custom_theme

apply_custom_theme()

current_user = st.session_state.get("user_id")

if not current_user:
    # ── 비로그인: 깔끔한 중앙 정렬 로그인 폼 ──
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    _, col_center, _ = st.columns([1, 1.4, 1])
    with col_center:
        st.image("assets/auth_hero.jpg", width="stretch")
        st.markdown("### 👤 사용자 로그인")
        st.caption("AI Assistant와 함께 개인화된 대화 세션과 스마트한 작업을 경험해보세요.")

        with st.container(border=True):
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
    # ── 로그인 후: 계정 정보 카드 ──
    st.title(f"👤 계정 관리")

    _, col_center, _ = st.columns([1, 1.6, 1])
    with col_center:
        st.image("assets/auth_hero.jpg", width="stretch")

        with st.container(border=True):
            st.subheader("접속 정보")
            st.metric(label="로그인 계정", value=current_user)
            has_key = bool(st.session_state.get("openai_api_key"))
            st.metric(label="API Key 상태", value="등록됨 ✅" if has_key else "미등록 ⚠️")

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("💬 채팅하러 가기", use_container_width=True, type="primary"):
                st.switch_page("pages_app2/chat.py")
        with col_b:
            if st.button("🔑 API Key 관리", use_container_width=True):
                st.switch_page("pages_app2/key_settings.py")

        if st.button("🚪 로그아웃", use_container_width=True):
            st.session_state.pop("user_id", None)
            st.session_state.pop("openai_api_key", None)
            st.session_state.pop("current_session_id", None)
            st.rerun()
