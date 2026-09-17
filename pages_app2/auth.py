import streamlit as st
from utils.db import get_user_sessions
from utils.ui_theme import apply_custom_theme

apply_custom_theme()

current_user = st.session_state.get("user_id")

if not current_user:
    # 1. 비로그인 상태: 세련된 중앙 로그인 카드 뷰
    _, center_col, _ = st.columns([1, 2.2, 1])
    with center_col:
        st.markdown(
            """
            <div style="text-align: center; margin-top: 20px; margin-bottom: 24px;">
                <div style="font-size: 3rem; margin-bottom: 8px;">🤖</div>
                <h1 style="font-size: 1.8rem; font-weight: 800; margin-bottom: 6px; letter-spacing: -0.5px;">AI Studio에 오신 것을 환영합니다</h1>
                <p style="color: gray; font-size: 0.95rem;">독립된 대화 세션과 안전한 AI 어시스턴트 환경을 경험하세요.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.markdown("#### 👤 사용자 로그인")
            username_input = st.text_input(
                "사용자 ID 또는 닉네임",
                placeholder="예: alex, user99, data_analyst",
                help="입력한 ID를 기준으로 대화 세션과 기록이 완전히 격리되어 저장됩니다.",
            )

            login_btn = st.button("🚀 로그인 및 시작하기", use_container_width=True, type="primary")
            if login_btn:
                if username_input.strip():
                    st.session_state["user_id"] = username_input.strip()
                    st.rerun()
                else:
                    st.warning("사용자 ID를 입력해주세요.")

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        # 주요 강점 3종 미니 카드
        f1, f2, f3 = st.columns(3)
        with f1:
            st.markdown(
                """
                <div class="glass-card" style="text-align: center; padding: 14px;">
                    <div style="font-size: 1.4rem;">🛡️</div>
                    <div style="font-weight: 700; font-size: 0.85rem; margin-top: 4px;">Zero DB 저장</div>
                    <div style="font-size: 0.75rem; color: gray; margin-top: 2px;">Key 메모리 보관</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with f2:
            st.markdown(
                """
                <div class="glass-card" style="text-align: center; padding: 14px;">
                    <div style="font-size: 1.4rem;">💬</div>
                    <div style="font-weight: 700; font-size: 0.85rem; margin-top: 4px;">스마트 세션</div>
                    <div style="font-size: 0.75rem; color: gray; margin-top: 2px;">최대 10개 대화 보관</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with f3:
            st.markdown(
                """
                <div class="glass-card" style="text-align: center; padding: 14px;">
                    <div style="font-size: 1.4rem;">⚡</div>
                    <div style="font-weight: 700; font-size: 0.85rem; margin-top: 4px;">GPT-5.6-Luna</div>
                    <div style="font-size: 0.75rem; color: gray; margin-top: 2px;">실시간 스트리밍</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

else:
    # 2. 로그인 완료 상태: 사용자 대시보드 및 바로가기 허브
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, rgba(79, 70, 229, 0.08) 0%, rgba(124, 58, 237, 0.08) 100%); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 16px; padding: 24px; margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                <div>
                    <h2 style="margin: 0; font-size: 1.6rem; font-weight: 800;">👋 안녕하세요, {current_user} 님!</h2>
                    <p style="margin: 6px 0 0 0; color: gray; font-size: 0.95rem;">오늘도 스마트한 AI 어시스턴트와 함께 생산성을 극대화해보세요.</p>
                </div>
                <div>
                    <span class="status-chip status-active">● 온라인 세션 활성화</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 사용자 계정 통계 지표
    sessions = get_user_sessions(current_user)
    total_messages = sum(s[3] for s in sessions)
    has_key = bool(st.session_state.get("openai_api_key"))

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric("📂 활성 대화 세션", f"{len(sessions)} / 10개")
    with col_m2:
        st.metric("💬 총 누적 메시지 수", f"{total_messages}개")
    with col_m3:
        st.metric("🔑 API Key 보관 상태", "정상 등록됨" if has_key else "미등록")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.subheader("🚀 빠른 서비스 이동")

    # 3개 서비스 바로가기 카드
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.markdown("### 💬 AI 챗봇")
            st.caption("GPT-5.6-Luna와 실시간 스트리밍 대화를 나누거나 이전 대화를 이어갑니다.")
            if st.button("채팅방 입장하기", use_container_width=True, type="primary"):
                st.switch_page("pages_app2/chat.py")

    with col2:
        with st.container(border=True):
            st.markdown("### 🔑 API Key 관리")
            st.caption("세션 메모리에 안전하게 OpenAI API Key를 등록하거나 파기합니다.")
            if st.button("Key 설정 바로가기", use_container_width=True):
                st.switch_page("pages_app2/key_settings.py")

    with col3:
        with st.container(border=True):
            st.markdown("### 📜 대화 기록실")
            st.caption("지난 대화 기록을 타임라인 또는 표 형태로 조회하고 내보냅니다.")
            if st.button("히스토리 열람하기", use_container_width=True):
                st.switch_page("pages_app2/history.py")

    st.divider()

    # 계정 관리
    with st.container(border=True):
        st.markdown("#### ⚙️ 계정 및 세션 관리")
        st.write("다른 계정으로 전환하거나 안전하게 세션을 종료하려면 아래 로그아웃을 이용하세요.")
        if st.button("🚪 안전하게 로그아웃하기", use_container_width=False):
            st.session_state.pop("user_id", None)
            st.session_state.pop("openai_api_key", None)
            st.session_state.pop("current_session_id", None)
            st.rerun()
