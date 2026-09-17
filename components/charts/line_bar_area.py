import streamlit as st
import pandas as pd
import numpy as np

def show_line_bar_area():
    st.header("📈 기본 내장 차트 (Line, Bar, Area Charts)")
    st.caption("복잡한 차트 라이브러리 설정 없이도 데이터프레임을 바로 시각화할 수 있는 강력한 내장 차트들입니다.")

    # 20일간의 3개 지점 트래픽 데이터 생성
    np.random.seed(42)
    chart_data = pd.DataFrame(
        np.random.randn(20, 3).cumsum(axis=0) + 50,
        columns=["서울 지점", "부산 지점", "대구 지점"],
    )

    # 1. 꺾은선 차트 (st.line_chart)
    st.subheader("1. 꺾은선형 차트 (st.line_chart)")
    st.line_chart(chart_data)

    # 2. 막대 차트 (st.bar_chart)
    st.subheader("2. 막대 차트 (st.bar_chart)")
    monthly_sales = pd.DataFrame({
        "월": ["1월", "2월", "3월", "4월", "5월", "6월"],
        "매출": [120, 150, 180, 130, 210, 240],
    }).set_index("월")
    st.bar_chart(monthly_sales)

    # 3. 영역 차트 (st.area_chart)
    st.subheader("3. 영역 차트 (st.area_chart)")
    st.area_chart(chart_data[["서울 지점", "부산 지점"]])

