import streamlit as st
from utils.db import init_db
from utils.ui_theme import apply_custom_theme

# 1. DB 초기화
init_db()

st.set_page_config(
    page_title="AI 챗봇",
    page_icon="💬",
    layout="wide",
)
apply_custom_theme()

# 네비게이션 로고 이미지 등록
st.logo("assets/logo.jpg", icon_image="assets/logo.jpg")

# 2. 로그인 여부 확인 및 상단 네비게이션 구성
user_id = st.session_state.get("user_id")

if not user_id:
    # 비로그인 시: 상단에 로그인 페이지만 노출
    login_page = st.Page("pages_app2/auth.py", title="로그인", icon="👤", default=True)
    pg = st.navigation([login_page], position="top")
else:
    # 로그인 시: 상단 네비게이션바에 주요 페이지 수평 배치
    chat_page = st.Page("pages_app2/chat.py", title="채팅", icon="💬", default=True)
    key_page = st.Page("pages_app2/key_settings.py", title="API Key", icon="🔑")
    history_page = st.Page("pages_app2/history.py", title="대화 내역", icon="📜")
    auth_page = st.Page("pages_app2/auth.py", title=f"계정 ({user_id})", icon="👤")

    # 상단(top) 네비게이션 적용 (사이드바는 각 페이지별 고유 옵션 전용으로 비워둠)
    pg = st.navigation([chat_page, key_page, history_page, auth_page], position="top")

# 페이지 실행
pg.run()
