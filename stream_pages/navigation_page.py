import streamlit as st


# ─── 1. 개별 페이지 함수 정의 ───
def show_home_page():
    st.title("🧭 Navigation & Pages 쇼케이스")
    st.caption(
        "Streamlit 공식 네비게이션 API (st.navigation, st.Page, st.page_link, st.switch_page) 예시입니다."
    )

    st.markdown("---")

    # [1] st.page_link 쇼케이스
    st.subheader("1️⃣ 페이지 링크 (`st.page_link`)")
    st.caption("사용자가 클릭하여 다른 내부 페이지나 외부 웹사이트로 이동할 수 있는 링크 컴포넌트입니다.")

    col1, col2 = st.columns(2)
    with col1:
        st.write("**내부 페이지 링크**")
        st.page_link(
            detail_page,
            label="상세 안내 페이지로 이동",
            icon=":material/description:",
            help="클릭 시 상세 안내 페이지로 이동합니다.",
        )
        st.page_link(
            settings_page,
            label="설정 페이지로 이동 (전체 너비)",
            icon=":material/settings:",
            use_container_width=True,
        )
        st.page_link(
            detail_page,
            label="비활성화된 링크 예시",
            icon=":material/block:",
            disabled=True,
            help="disabled=True 설정 시 비활성화됩니다.",
        )

    with col2:
        st.write("**외부 URL 링크**")
        st.page_link(
            "https://docs.streamlit.io/develop/api-reference/navigation",
            label="Streamlit Navigation 공식 문서",
            icon=":material/open_in_new:",
            help="공식 문서 웹페이지가 새 탭으로 열립니다.",
        )
        st.page_link(
            "https://streamlit.io",
            label="Streamlit 공식 웹사이트",
            icon=":material/public:",
        )

    st.markdown("---")

    # [2] st.switch_page 쇼케이스
    st.subheader("2️⃣ 프로그래밍 방식 페이지 전환 (`st.switch_page`)")
    st.caption("버튼 클릭 등 특정 로직 실행 후 코드로 즉시 대상 페이지로 전환합니다.")

    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("🚀 상세 페이지로 전환 (st.switch_page)", type="primary", use_container_width=True):
            st.switch_page(detail_page)

    with btn_col2:
        if st.button("⚙️ 설정 페이지로 전환 (st.switch_page)", use_container_width=True):
            st.switch_page(settings_page)


def show_detail_page():
    st.title("📄 상세 안내 페이지 (Detail Page)")
    st.caption("`st.page_link` 또는 `st.switch_page`를 통해 이동해온 대상 페이지입니다.")

    st.info("이 페이지는 `st.Page` 객체로 정의되어 네비게이션에 등록된 페이지입니다.")

    st.subheader("🔙 이전 페이지로 돌아가기")
    st.page_link(home_page, label="홈으로 이동 (st.page_link)", icon=":material/arrow_back:")

    if st.button("홈으로 이동 (st.switch_page)"):
        st.switch_page(home_page)


def show_settings_page():
    st.title("⚙️ 환경 설정 페이지 (Settings Page)")
    st.caption("네비게이션 메뉴를 통해 접근할 수 있는 보조 페이지 예시입니다.")

    theme_option = st.selectbox("테마 모드 선택", ["시스템 기본", "라이트 모드", "다크 모드"])
    notification = st.toggle("알림 활성화", value=True)

    st.write(f"- 선택된 테마: **{theme_option}**")
    st.write(f"- 알림 수신 여부: **{notification}**")

    st.divider()
    st.page_link(home_page, label="홈으로 돌아가기", icon=":material/home:")


# ─── 2. 페이지 객체 생성 (st.Page) ───
home_page = st.Page(
    show_home_page,
    title="홈 (Home)",
    icon=":material/home:",
    url_path="home",
    default=True,
)

detail_page = st.Page(
    show_detail_page,
    title="상세 안내 (Detail)",
    icon=":material/description:",
    url_path="detail",
)

settings_page = st.Page(
    show_settings_page,
    title="환경 설정 (Settings)",
    icon=":material/settings:",
    url_path="settings",
)


# ─── 3. 네비게이션 구성 및 실행 (st.navigation) ───
# 딕셔너리를 사용하여 카테고리(섹션)별로 페이지 분류 구성
pg = st.navigation(
    {
        "메인": [home_page],
        "보조 메뉴": [detail_page, settings_page],
    },
    position="sidebar",  # "sidebar", "top", "hidden"
    expanded=True,
)

# 선택된 페이지 실행
pg.run()

