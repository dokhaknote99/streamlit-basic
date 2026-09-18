import streamlit as st

st.title("ℹ️ 프로젝트 소개 (About)")
st.caption("Streamlit 기본 기능 및 네비게이션 실습 프로젝트입니다.")

st.markdown("---")

st.markdown(
    """
    ### 📌 구성된 주요 기능
    1. **사용자 인증 (Authentication)**: `st.login`, `st.logout`, `st.user` (Google OIDC)
    2. **멀티페이지 라우팅**: `st.navigation`, `st.Page`
    3. **페이지 이동 제어**: `st.page_link`, `st.switch_page`
    """
)

st.markdown("---")

st.page_link(
    "https://docs.streamlit.io",
    label="Streamlit 공식 문서 바로가기",
    icon=":material/open_in_new:",
)
st.page_link("home_page.py", label="홈으로 돌아가기", icon=":material/home:")

