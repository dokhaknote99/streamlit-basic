import time
import streamlit as st

def show_progress_status():
    st.header("⏳ 진행 상태 표시 (Spinner, Progress, Status)")

    # 1. 로딩 스피너 (st.spinner)
    st.subheader("1. 로딩 스피너 (st.spinner)")
    st.caption("비동기 처리나 데이터 로딩 중 회전하는 스피너를 보여줍니다.")
    if st.button("2초 로딩 스피너 테스트"):
        with st.spinner("데이터를 분석하고 있습니다..."):
            time.sleep(2)
        st.success("데이터 분석 완료!")

    st.divider()

    # 2. 진행률 바 (st.progress)
    st.subheader("2. 진행률 바 (st.progress)")
    st.caption("작업의 퍼센트(0~100%) 진행도를 시각적으로 보여줍니다.")
    if st.button("진행률 바 애니메이션 시작"):
        progress_bar = st.progress(0, text="작업 진행 중...")
        for percent_complete in range(1, 101, 20):
            time.sleep(0.15)
            progress_bar.progress(percent_complete, text=f"작업 진행 중... {percent_complete}%")
        st.success("작업이 100% 완료되었습니다!")

    st.divider()

    # 3. 단계별 상태 컨테이너 (st.status)
    st.subheader("3. 단계별 진행 컨테이너 (st.status)")
    st.caption("여러 하위 단계로 이루어진 복합 작업의 실시간 진행 상황을 깔끔하게 보여줍니다.")
    if st.button("단계별 상태 테스트 실행"):
        with st.status("다운로드 진행 중...", expanded=True) as status:
            st.write("1단계: 서버에 연결하는 중...")
            time.sleep(1)
            st.write("2단계: 데이터를 다운로드하는 중...")
            time.sleep(1)
            st.write("3단계: 데이터 무결성을 검증하는 중...")
            time.sleep(1)
            status.update(label="모든 다운로드 및 검증이 완료되었습니다!", state="complete", expanded=False)

