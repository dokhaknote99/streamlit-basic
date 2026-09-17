import streamlit as st
from utils.db import init_db

# 1. DB 초기화 (테이블 및 스키마 준비)
init_db()

st.set_page_config(
    page_title="OpenAI AI 챗봇 시스템",
    page_icon="💬",
    layout="wide",
)

# 2. 로그인 여부 확인 및 네비게이션 분기
user_id = st.session_state.get("user_id")

if not user_id:
    # 비로그인 상태: 로그인 페이지만 활성화
    login_page = st.Page("pages_app2/auth.py", title="로그인", icon="👤", default=True)
    pg = st.navigation([login_page])
else:
    # 로그인 상태: 사이드바 사용자 프로필 및 로그아웃 버튼 배치
    with st.sidebar:
        st.write(f"👤 접속자: **{user_id}** 님")
        key_status = "✅ 등록됨 (메모리)" if st.session_state.get("openai_api_key") else "⚠️ 미등록"
        st.caption(f"API Key: {key_status}")

        if st.button("🚪 로그아웃", use_container_width=True):
            st.session_state.pop("user_id", None)
            st.session_state.pop("openai_api_key", None)
            st.session_state.pop("current_session_id", None)
            st.rerun()
        st.divider()

    # 로그인 후 이용 가능한 공식 페이지 정의
    chat_page = st.Page("pages_app2/chat.py", title="AI 챗봇", icon="💬", default=True)
    key_page = st.Page("pages_app2/key_settings.py", title="API Key 등록", icon="🔑")
    history_page = st.Page("pages_app2/history.py", title="과거 대화 내역", icon="📜")
    auth_page = st.Page("pages_app2/auth.py", title="내 계정 정보", icon="👤")

    pg = st.navigation({
        "💬 서비스": [chat_page, key_page],
        "📜 데이터 관리": [history_page],
        "👤 계정": [auth_page],
    })

# 네비게이션 실행
pg.run()
