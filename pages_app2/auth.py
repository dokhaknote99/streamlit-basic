import streamlit as st
from utils.ui_theme import apply_custom_theme, page_header

apply_custom_theme()

current_user = st.session_state.get("user_id")

if not current_user:
    # ── 비로그인: 중앙 정렬 로그인 카드 ──
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

    _, col_center, _ = st.columns([1, 1.15, 1])
    with col_center:
        with st.container(border=True, key="card_login"):
            st.image("assets/auth_hero.jpg", width="stretch")
            st.markdown("### 환영합니다 👋")
            st.caption("AI Assistant와 함께 개인화된 대화 세션과 스마트한 작업을 경험해보세요.")

            username_input = st.text_input(
                "사용자 ID",
                placeholder="아이디 또는 닉네임을 입력하세요",
                icon=":material/person:",
            )
            if st.button("로그인", width="stretch", type="primary"):
                if username_input.strip():
                    st.session_state["user_id"] = username_input.strip()
                    st.rerun()
                else:
                    st.warning("사용자 ID를 입력해주세요.")

        st.caption(
            "별도의 비밀번호 없이 ID만으로 대화 세션이 분리됩니다. 공용 PC에서는 사용 후 로그아웃해주세요.",
            text_alignment="center",
        )

else:
    # ── 로그인 후: 계정 정보 + 바로가기 ──
    has_key = bool(st.session_state.get("openai_api_key"))
    page_header(
        "👤",
        "계정 관리",
        "현재 접속 정보와 API Key 상태를 확인하고 주요 기능으로 바로 이동할 수 있어요.",
    )

    col_left, col_right = st.columns([1.15, 1], gap="medium")

    with col_left:
        with st.container(border=True, key="card_account"):
            st.image("assets/auth_hero.jpg", width="stretch")
            st.markdown("#### 접속 정보")
            m1, m2 = st.columns(2)
            with m1:
                st.metric(label="로그인 계정", value=current_user, icon=":material/account_circle:")
            with m2:
                st.metric(
                    label="API Key",
                    value="등록됨" if has_key else "미등록",
                    icon=":material/key:" if has_key else ":material/key_off:",
                )

    with col_right:
        with st.container(border=True, key="card_shortcuts"):
            st.markdown("#### 바로가기")
            st.caption("자주 쓰는 기능으로 한 번에 이동하세요.")
            if st.button("채팅하러 가기", icon=":material/chat:", width="stretch", type="primary"):
                st.switch_page("pages_app2/chat.py")
            if st.button("API Key 관리", icon=":material/key:", width="stretch"):
                st.switch_page("pages_app2/key_settings.py")
            if st.button("대화 내역 보기", icon=":material/history:", width="stretch"):
                st.switch_page("pages_app2/history.py")

        with st.container(border=True, key="card_logout"):
            st.markdown("#### 세션 종료")
            st.caption("로그아웃하면 브라우저에 보관된 API Key도 함께 삭제됩니다.")
            if st.button("로그아웃", icon=":material/logout:", width="stretch"):
                st.session_state.pop("user_id", None)
                st.session_state.pop("openai_api_key", None)
                st.session_state.pop("current_session_id", None)
                st.rerun()
