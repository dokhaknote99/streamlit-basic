import streamlit as st

def show_columns():
    st.header("🏛️ 다단 컬럼 레이아웃 (st.columns)")
    st.write("화면을 가로로 분할하여 요소를 나란히 배치합니다.")

    # 1. 동일 비율 3분할
    st.subheader("1. 동일 비율 분할 (1:1:1)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📌 컬럼 1")
        st.button("버튼 A")
    with col2:
        st.success("📌 컬럼 2")
        st.text_input("입력 B", value="내용")
    with col3:
        st.warning("📌 컬럼 3")
        st.write("단순 텍스트")

    # 2. 비율 지정 및 수직 정렬, 간격(gap)
    st.subheader("2. 비율 지정 [3, 1] & 수직 중앙 정렬 (vertical_alignment='center')")
    c_left, c_right = st.columns([3, 1], vertical_alignment="center", gap="medium")
    with c_left:
        st.text_input("검색어 입력 (넓은 영역)", placeholder="검색어를 입력하세요")
    with c_right:
        st.button("🔍 검색", use_container_width=True)

