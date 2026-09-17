import streamlit as st

st.set_page_config(
    page_title="OpenAI AI 챗봇 시스템",
    page_icon="💬",
    layout="wide",
)

# Streamlit 공식 멀티페이지 네비게이션 정의 (st.navigation & st.Page)
chat_page = st.Page("app2_chat.py", title="AI 챗봇 대화", icon="💬", default=True)
history_page = st.Page("app2_history.py", title="과거 대화 내역", icon="📜")

# 사이드바 네비게이션 메뉴 구성 및 실행
pg = st.navigation({
    "💬 챗봇 서비스": [chat_page],
    "📜 데이터 관리": [history_page],
})

pg.run()
