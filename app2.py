import streamlit as st
from utils.db import init_db
from utils.ui_theme import apply_custom_theme

init_db()

st.set_page_config(
    page_title="AI 챗봇",
    page_icon="💬",
    layout="wide",
)
apply_custom_theme()

user_id = st.session_state.get("user_id")

if not user_id:
    login_page = st.Page("pages_app2/auth.py", title="로그인", icon="👤", default=True)
    pg = st.navigation([login_page])
else:
    # 플랫한 단일 페이지 목록 (목차/그룹핑 헤더 제거)
    chat_page = st.Page("pages_app2/chat.py", title="채팅", icon="💬", default=True)
    key_page = st.Page("pages_app2/key_settings.py", title="API Key 등록", icon="🔑")
    history_page = st.Page("pages_app2/history.py", title="대화 내역", icon="📜")
    auth_page = st.Page("pages_app2/auth.py", title="계정", icon="👤")

    pg = st.navigation([chat_page, key_page, history_page, auth_page])

    with st.sidebar:
        st.markdown(f"**👤 {user_id}** 님")
        if st.session_state.get("openai_api_key"):
            st.caption("🔑 API Key: 등록됨")
        else:
            st.caption("⚠️ API Key: 미등록")

        if st.button("로그아웃", use_container_width=True):
            st.session_state.pop("user_id", None)
            st.session_state.pop("openai_api_key", None)
            st.session_state.pop("current_session_id", None)
            st.rerun()
        st.divider()

pg.run()
