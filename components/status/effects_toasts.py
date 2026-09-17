import streamlit as st

def show_effects_toasts():
    st.header("🎉 토스트 알림 & 축하 이펙트 (Toast, Balloons, Snow)")

    # 1. 토스트 팝업 (st.toast)
    st.subheader("1. 토스트 알림 (st.toast)")
    st.caption("화면 우측 하단에 잠깐 떴다가 사라지는 가벼운 알림 메시지입니다.")
    if st.button("토스트 알림 띄우기"):
        st.toast("저장되었습니다!", icon="💾")

    st.divider()

    # 2. 축하 풍선 애니메이션 (st.balloons)
    st.subheader("2. 풍선 이펙트 (st.balloons)")
    if st.button("🎈 축하 풍선 날리기"):
        st.balloons()

    st.divider()

    # 3. 눈 내리는 애니메이션 (st.snow)
    st.subheader("3. 눈송이 이펙트 (st.snow)")
    if st.button("❄️ 눈송이 날리기"):
        st.snow()

