import streamlit as st

st.title("⚙️ 환경 설정 (Settings)")
st.caption("애플리케이션 환경 설정을 시뮬레이션하는 페이지입니다.")

st.markdown("---")

theme = st.selectbox("UI 테마 선택", ["시스템 기본", "라이트", "다크"])
auto_save = st.toggle("자동 저장 활성화", value=True)
items_per_page = st.slider("페이지 당 항목 수", min_value=5, max_value=50, value=20, step=5)

st.write(f"- 테마: **{theme}**")
st.write(f"- 자동 저장: **{'ON' if auto_save else 'OFF'}**")
st.write(f"- 목록 수: **{items_per_page}개**")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.page_link("home_page.py", label="홈으로 돌아가기 (st.page_link)", icon=":material/home:")
with col2:
    if st.button("홈으로 이동 (st.switch_page)", use_container_width=True):
        st.switch_page("home_page.py")

