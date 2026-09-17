import streamlit as st

def show_expanders_popovers():
    st.header("📑 접기/펼치기 & 팝오버 (Expander, Popover, Tabs)")

    # 1. 아코디언 (st.expander)
    st.subheader("1. 접기/펼치기 아코디언 (st.expander)")
    with st.expander("ℹ️ 기본 펼치기 메뉴 (클릭해서 열기/닫기)"):
        st.write("숨겨져 있던 상세 설명이나 코드가 여기에 나타납니다.")
        st.code("print('Hello Streamlit!')", language="python")

    with st.expander("💡 처음부터 펼쳐진 아코디언 (expanded=True)", expanded=True, icon="💡"):
        st.write("이 영역은 페이지가 로드될 때 기본으로 펼쳐져 있습니다.")

    st.divider()

    # 2. 팝오버 팝업창 (st.popover)
    st.subheader("2. 팝오버 버튼 (st.popover)")
    st.write("버튼을 누르면 화면 위에 작은 오버레이 팝업창이 열립니다.")

    with st.popover("⚙️ 간편 설정 열기", icon="⚙️"):
        st.write("팝오버 내부 설정 메뉴")
        theme = st.selectbox("테마 선택", ["라이트", "다크", "시스템 기본"])
        noti = st.toggle("알림 활성화", value=True)
        st.write(f"설정 상태: 테마={theme}, 알림={noti}")

    st.divider()

    # 3. 중첩 탭 (st.tabs)
    st.subheader("3. 탭 컴포넌트 자체 활용 (st.tabs)")
    sub_tab1, sub_tab2 = st.tabs(["서브 탭 A", "서브 탭 B"])
    with sub_tab1:
        st.write("여기는 '서브 탭 A'의 내용입니다.")
    with sub_tab2:
        st.write("여기는 '서브 탭 B'의 내용입니다.")

