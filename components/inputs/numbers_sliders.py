import streamlit as st

def show_numbers_sliders():
    st.header("🔢 숫자 입력 (st.number_input)")

    st.subheader("1. 기본 정수 입력")
    num_int = st.number_input(label="나이 입력", value=25)
    st.write("👉 입력값:", num_int)

    st.subheader("2. 최소값/최대값/증감단위 (min_value, max_value, step)")
    qty = st.number_input(
        label="주문 수량 (1 ~ 50개, 5개 단위)",
        min_value=1,
        max_value=50,
        value=5,
        step=5,
    )
    st.write("👉 선택한 수량:", qty)

    st.subheader("3. 소수점 입력 및 포맷 (format='%.2f')")
    rating = st.number_input(
        label="평점 (0.00 ~ 5.00)",
        min_value=0.0,
        max_value=5.0,
        value=4.5,
        step=0.1,
        format="%.2f",
    )
    st.write("👉 입력된 평점:", rating)

    st.divider()

    st.header("🎚️ 슬라이더 (st.slider & st.select_slider)")

    st.subheader("1. 기본 정수 슬라이더")
    volume = st.slider(label="볼륨 조절", min_value=0, max_value=100, value=50)
    st.write("👉 현재 볼륨:", volume)

    st.subheader("2. 소수점(실수) 슬라이더")
    temperature = st.slider(
        label="목표 온도 (°C)",
        min_value=-10.0,
        max_value=40.0,
        value=22.5,
        step=0.5,
    )
    st.write("👉 설정 온도:", temperature)

    st.subheader("3. 범위 선택 슬라이더 (Range Slider)")
    st.caption("초기값(value)에 (시작, 끝) 튜플을 넘기면 양쪽 조절 핸들이 생깁니다.")
    price_range = st.slider(
        label="가격대 범위 선택 (만원)",
        min_value=0,
        max_value=200,
        value=(30, 100),
    )
    st.write("👉 선택된 범위 (시작, 끝):", price_range)

    st.subheader("4. 항목 선택 슬라이더 (st.select_slider)")
    satisfaction = st.select_slider(
        label="서비스 만족도",
        options=["매우 불만", "불만", "보통", "만족", "매우 만족"],
        value="보통",
    )
    st.write("👉 선택한 만족도:", satisfaction)

    st.subheader("5. 항목 범위 선택 슬라이더")
    size_range = st.select_slider(
        label="의류 사이즈 범위 선택",
        options=["XS", "S", "M", "L", "XL", "XXL"],
        value=("S", "XL"),
    )
    st.write("👉 선택된 사이즈 범위:", size_range)

