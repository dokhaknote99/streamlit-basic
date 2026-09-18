import streamlit as st

st.title("🏠 홈 (Home)")
st.caption("여러 페이지 파일을 네비게이션으로 연결한 Streamlit 멀티페이지 앱입니다.")

st.markdown("---")

st.subheader("🔗 빠른 이동 (`st.page_link`)")
st.caption("사이드바 메뉴 외에도 본문에서 다른 페이지로 직접 이동할 수 있습니다.")

col1, col2 = st.columns(2)
with col1:
    st.page_link(
        "auth_page.py",
        label="로그인 / 사용자 인증 페이지",
        icon=":material/lock:",
        use_container_width=True,
    )
    st.page_link(
        "settings_page.py",
        label="환경 설정 페이지",
        icon=":material/settings:",
        use_container_width=True,
    )

with col2:
    st.page_link(
        "about_page.py",
        label="프로젝트 소개 페이지",
        icon=":material/info:",
        use_container_width=True,
    )
    st.page_link(
        "https://docs.streamlit.io/develop/api-reference/navigation",
        label="Streamlit Navigation 공식 문서 (외부)",
        icon=":material/open_in_new:",
        use_container_width=True,
    )

st.markdown("---")

st.subheader("🚀 프로그래밍 방식 전환 (`st.switch_page`)")
st.caption("버튼 클릭 후 코드 로직에 따라 즉시 특정 페이지로 전환합니다.")

btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    if st.button("🔐 로그인 페이지로 바로 이동", type="primary", use_container_width=True):
        st.switch_page("auth_page.py")

with btn_col2:
    if st.button("⚙️ 설정 페이지로 바로 이동", use_container_width=True):
        st.switch_page("settings_page.py")

