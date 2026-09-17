import datetime
import streamlit as st

def show_date_time_extras():
    st.header("📅 날짜 & 시간 입력 (st.date_input, st.time_input)")

    st.subheader("1. 단일 날짜 선택 (st.date_input)")
    appointment = st.date_input(
        label="방문 예약일",
        value=datetime.date.today(),
        min_value=datetime.date.today(),
    )
    st.write("👉 예약 날짜:", appointment)

    st.subheader("2. 날짜 범위 선택 (시작일, 종료일 튜플 전달)")
    st.caption("초기값으로 (시작일, 종료일) 튜플을 넘기면 달력에서 기간을 드래그해 선택할 수 있습니다.")
    today = datetime.date.today()
    vacation = st.date_input(
        label="휴가 일정",
        value=(today, today + datetime.timedelta(days=3)),
        format="YYYY/MM/DD",
    )
    st.write("👉 선택된 휴가 일정:", vacation)

    st.subheader("3. 시간 입력 (st.time_input)")
    meeting_time = st.time_input(
        label="회의 시작 시간",
        value=datetime.time(9, 30),
        step=datetime.timedelta(minutes=15),
    )
    st.write("👉 선택된 회의 시간:", meeting_time)

    st.divider()

    st.header("🎨 기타 위젯: 색상 선택 (st.color_picker)")
    picked_color = st.color_picker(
        label="테마 색상을 골라보세요",
        value="#00f900",
        help="HEX 색상 코드를 직접 입력하거나 팔레트에서 선택할 수 있습니다.",
    )
    st.write("👉 선택된 HEX 색상 코드:", picked_color)

