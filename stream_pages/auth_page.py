import streamlit as st

st.title("🔐 사용자 인증 (Authentication)")
st.caption("공식 API(st.login, st.logout, st.user)를 활용한 사용자 로그인 기능 예시입니다.")

st.markdown("---")

# 1. 로그인 여부 확인 (st.user.is_logged_in)
if not st.user.is_logged_in:
    st.info("로그인이 필요합니다. 아래 버튼을 눌러 Google 로그인을 진행해주세요.")

    if st.button("Google 계정으로 로그인", icon=":material/login:", type="primary"):
        st.login("google")

else:
    # 2. 로그인된 사용자 정보 확인 (st.user)
    st.success(f"환영합니다, {st.user.name}님!")

    st.subheader("👤 사용자 정보 (`st.user`)")
    st.write(f"- **이름 (name)**: {st.user.name}")
    st.write(f"- **이메일 (email)**: {st.user.email}")
    st.write(f"- **로그인 여부 (is_logged_in)**: {st.user.is_logged_in}")

    with st.expander("전체 사용자 데이터 (to_dict)", expanded=False):
        st.json(st.user.to_dict())

    # 3. 로그아웃 (st.logout)
    if st.button("로그아웃", icon=":material/logout:"):
        st.logout()

    st.markdown("---")
    st.page_link("home_page.py", label="홈으로 이동", icon=":material/home:")
