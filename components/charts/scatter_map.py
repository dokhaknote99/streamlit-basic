import streamlit as st
import pandas as pd
import numpy as np

def show_scatter_map():
    st.header("🗺️ 산점도 및 지도 시각화 (st.scatter_chart & st.map)")

    # 1. 산점도 차트 (st.scatter_chart)
    st.subheader("1. 산점도 차트 (st.scatter_chart)")
    np.random.seed(10)
    scatter_df = pd.DataFrame({
        "광고비": np.random.randint(10, 100, 30),
        "매출액": np.random.randint(50, 300, 30),
        "팀규모": np.random.randint(2, 10, 30) * 10,
    })
    st.scatter_chart(scatter_df, x="광고비", y="매출액", size="팀규모")

    st.divider()

    # 2. 지도 시각화 (st.map)
    st.subheader("2. 지도 위 위치 표시 (st.map)")
    st.caption("위도(latitude)와 경도(longitude) 데이터가 있는 데이터프레임을 주면 지도 위에 점을 찍어줍니다.")

    # 서울 시청 인근 좌표 데이터
    seoul_locations = pd.DataFrame({
        "latitude": [37.5665 + np.random.randn() * 0.01 for _ in range(15)],
        "longitude": [126.9780 + np.random.randn() * 0.01 for _ in range(15)],
    })
    st.map(seoul_locations)

