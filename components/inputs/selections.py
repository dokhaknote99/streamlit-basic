import streamlit as st

def show_selections():
    st.header("🔘 선택 위젯 (st.radio, st.selectbox, st.multiselect)")

    st.subheader("1. 라디오 버튼 (st.radio)")
    radio_fruit = st.radio(
        label="좋아하는 과일을 선택하세요",
        options=["사과", "바나나", "딸기"],
        index=0,
    )
    st.write("👉 선택한 과일:", radio_fruit)

    st.write("가로 배치(horizontal=True) 및 보충 설명(captions):")
    delivery = st.radio(
        label="배송 방법 선택",
        options=["일반 배송", "새벽 배송", "당일 퀵 배송"],
        captions=["2~3일 소요 (무료)", "내일 아침 7시 전 도착 (+3,000원)", "오늘 저녁 도착 (+5,000원)"],
        horizontal=True,
    )
    st.write("👉 선택한 배송:", delivery)

    st.subheader("2. 선택박스 (st.selectbox)")
    country = st.selectbox(
        label="거주 국가 선택",
        options=["대한민국", "미국", "일본", "독일", "프랑스"],
        index=0,
    )
    st.write("👉 선택된 국가:", country)

    st.write("비어있는 상태로 시작 (index=None & placeholder):")
    selected_job = st.selectbox(
        label="직업 선택",
        options=["개발자", "디자이너", "기획자", "학생"],
        index=None,
        placeholder="직업을 선택해주세요...",
    )
    st.write("👉 선택된 직업:", selected_job)

    st.subheader("3. 다중 선택박스 (st.multiselect)")
    hobbies = st.multiselect(
        label="취미를 모두 선택하세요",
        options=["독서", "영화 감상", "운동", "게임", "음악 감상", "여행"],
        default=["독서", "여행"],
    )
    st.write("👉 선택된 취미들:", hobbies)

    st.write("최대 선택 개수 제한 (max_selections=2):")
    skills = st.multiselect(
        label="주요 프로그래밍 언어 (최대 2개)",
        options=["Python", "JavaScript", "C++", "Java", "Go", "Rust"],
        max_selections=2,
    )
    st.write("👉 선택된 언어:", skills)

    st.subheader("4. 체크박스와 토글 (st.checkbox, st.toggle)")
    agree = st.checkbox("이용약관에 동의합니다", value=False)
    st.write("👉 동의 여부 (True/False):", agree)

    alarm = st.toggle("야간 알림 수신 허용", value=True)
    st.write("👉 토글 상태 (True/False):", alarm)

