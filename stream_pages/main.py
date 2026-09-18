import streamlit as st

# 1. 로그인 여부(st.user.is_logged_in)에 따라 동적으로 네비게이션 페이지 구성
if not st.user.is_logged_in:
    # 비로그인 상태: 로그인 페이지만 노출 및 접근 허용
    login_page = st.Page("auth_page.py", title="로그인", icon=":material/lock:", default=True)
    pg = st.navigation([login_page], position="sidebar")

else:
    # 로그인 완료 상태: 모든 서비스 페이지 접근 허용
    home_page = st.Page("home_page.py", title="홈", icon=":material/home:", default=True)
    account_page = st.Page(
        "auth_page.py",
        title=f"계정 관리 ({st.user.name})",
        icon=":material/account_circle:",
    )
    settings_page = st.Page("settings_page.py", title="환경 설정", icon=":material/settings:")
    about_page = st.Page("about_page.py", title="소개", icon=":material/info:")

    pg = st.navigation(
        {
            "메인": [home_page, account_page],
            "시스템": [settings_page, about_page],
        },
        position="sidebar",
        expanded=True,
    )

# 2. 현재 선택된 페이지 실행
pg.run()