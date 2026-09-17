import streamlit as st

def show_containers():
    st.header("📦 컨테이너 및 공간 조절 (Container, Space, Bottom)")

    # 1. 테두리가 있는 컨테이너
    st.subheader("1. 카드 스타일 테두리 컨테이너 (border=True)")
    with st.container(border=True):
        st.write("📦 **테두리가 있는 컨테이너 (border=True)**")
        st.write("관련된 위젯들을 하나의 박스로 깔끔하게 그룹화합니다.")
        st.checkbox("컨테이너 내부 체크박스")

    # 2. 스크롤 가능한 고정 높이 컨테이너
    st.subheader("2. 스크롤 가능한 고정 높이 컨테이너 (height=130)")
    with st.container(height=130, border=True):
        st.write("📜 스크롤 가능한 영역입니다.")
        st.write("1행: 내용이 넘치면")
        st.write("2행: 컨테이너 내부에")
        st.write("3행: 스크롤바가 생깁니다.")
        st.write("4행: 계속 스크롤해보세요.")
        st.write("5행: 마지막 라인")

    # 3. 여백 추가 (st.space)
    st.subheader("3. 요소 간 간격 추가 (st.space)")
    st.write("위쪽 요소")
    st.space("large")
    st.caption("↑ st.space('large')로 넓은 여백이 들어갔습니다.")
    st.write("아래쪽 요소")

    # 4. 화면 하단 고정 컨테이너 (st.bottom)
    st.subheader("4. 화면 하단 고정 컨테이너 (st.bottom)")
    st.caption("화면 맨 밑바닥에 고정 바(Footer/Status)를 띄웁니다.")
    with st.bottom:
        with st.container(border=True):
            st.caption("⚓ st.bottom 영역: 화면 맨 하단에 항상 고정 표시됩니다.")

