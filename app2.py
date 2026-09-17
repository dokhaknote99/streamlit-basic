import streamlit as st
from utils.db import init_db
from utils.ui_theme import apply_custom_theme

# 1. DB 초기화
init_db()

st.set_page_config(
    page_title="OpenAI AI 챗봇 시스템",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_custom_theme()

# 2. 로그인 여부 확인 및 네비게이션 분기
user_id = st.session_state.get("user_id")

if not user_id:
    # 비로그인 상태: 로그인 페이지만 활성화
    login_page = st.Page("pages_app2/auth.py", title="로그인", icon="👤", default=True)
    pg = st.navigation([login_page])
else:
    # 로그인 상태: 사이드바 사용자 프로필 및 상태 위젯 배치
    with st.sidebar:
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); padding: 14px 18px; border-radius: 12px; color: white; margin-bottom: 16px; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);">
                <div style="font-size: 1.15rem; font-weight: 700; letter-spacing: -0.5px;">🤖 AI Studio</div>
                <div style="font-size: 0.78rem; opacity: 0.9; margin-top: 2px;">Smart Assistant Suite</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        has_key = bool(st.session_state.get("openai_api_key"))
        key_badge = '<span class="status-chip status-active">🟢 Key 활성화</span>' if has_key else '<span class="status-chip status-inactive">⚠️ Key 미등록</span>'

        st.markdown(
            f"""
            <div style="background: rgba(128, 128, 128, 0.06); border: 1px solid rgba(128, 128, 128, 0.15); border-radius: 12px; padding: 12px 14px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-weight: 600; font-size: 0.95rem;">👤 {user_id}</span>
                    <span style="font-size: 0.75rem; color: #10b981; font-weight: 600;">● 온라인</span>
                </div>
                <div>{key_badge}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("🚪 로그아웃", use_container_width=True):
            st.session_state.pop("user_id", None)
            st.session_state.pop("openai_api_key", None)
            st.session_state.pop("current_session_id", None)
            st.rerun()

        st.divider()

    # 로그인 후 이용 가능한 공식 페이지 정의
    chat_page = st.Page("pages_app2/chat.py", title="AI 챗봇", icon="💬", default=True)
    key_page = st.Page("pages_app2/key_settings.py", title="API Key 관리", icon="🔑")
    history_page = st.Page("pages_app2/history.py", title="대화 기록 보관소", icon="📜")
    auth_page = st.Page("pages_app2/auth.py", title="내 프로필 대시보드", icon="👤")

    pg = st.navigation({
        "💬 대화 서비스": [chat_page, key_page],
        "📜 데이터 관리": [history_page],
        "👤 사용자 계정": [auth_page],
    })

# 네비게이션 실행
pg.run()
