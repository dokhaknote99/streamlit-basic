import streamlit as st
import pandas as pd

def show_write_basics():
    st.header("✍️ st.write (다목적 만능 출력 함수)")
    st.caption("st.write는 전달되는 데이터 타입(문자열, 숫자, 리스트, 딕셔너리, 데이터프레임 등)에 맞춰 자동으로 가장 알맞은 형식으로 화면에 표시합니다.")

    # 1. 일반 텍스트 및 마크다운
    st.subheader("1. 텍스트 및 기본 서식")
    st.write("일반 문자열뿐 아니라 **굵은 글씨**, *기울임*, :blue[색상 텍스트]도 지원합니다.")

    # 2. 숫자 및 여러 인자 전달
    st.subheader("2. 여러 인자 동시 출력")
    st.write("숫자 100과 200의 합은:", 100 + 200, "입니다.")

    # 3. 딕셔너리 및 데이터 구조
    st.subheader("3. 딕셔너리 (Key-Value) 자동 서식")
    st.write({
        "이름": "홍길동",
        "나이": 30,
        "취미": ["독서", "코딩"],
        "활성상태": True,
    })

    # 4. 데이터프레임 자동 테이블 변환
    st.subheader("4. 데이터프레임 자동 렌더링")
    df = pd.DataFrame({
        "과일": ["사과", "바나나", "체리"],
        "가격": [1000, 1500, 3000],
        "재고": [10, 25, 8],
    })
    st.write("st.write(df)로 데이터프레임을 바로 전달하면 인터랙티브 테이블이 됩니다:")
    st.write(df)

