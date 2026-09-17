import streamlit as st

def show_sidebars_empty():
    st.header("📌 사이드바 & 동적 교체 (Sidebar, Empty)")

    # 1. 사이드바 (st.sidebar)
    st.subheader("1. 사이드바 영역 제어 (st.sidebar)")
    st.write("화면 좌측 사이드바 영역에 위젯을 배치합니다. (좌측 사이드바 패널을 확인해보세요)")
    with st.sidebar:
        st.header("📌 사이드바 영역")
        st.caption("st.sidebar를 통해 좌측 패널에 추가된 위젯입니다.")
        side_text = st.text_input("사이드바 텍스트", value="사이드바 값")
        side_slider = st.slider("사이드바 슬라이더", 0, 100, 30)
        st.write("사이드바 값:", side_text, side_slider)

    st.divider()

    # 2. 동적 플레이스홀더 (st.empty)
    st.subheader("2. 동적 플레이스홀더 (st.empty)")
    st.write("특정 위치의 요소를 지우거나 다른 내용으로 실시간 교체할 때 사용합니다.")
    placeholder = st.empty()
    placeholder.info("🔄 현재 이 자리는 기본 안내 메시지입니다.")
    if st.button("플레이스홀더 내용 변경하기"):
        placeholder.success("🎉 버튼이 눌려 내용이 성공적으로 변경되었습니다!")

