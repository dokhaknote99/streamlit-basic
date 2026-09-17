import streamlit as st
from components.charts.line_bar_area import show_line_bar_area
from components.charts.scatter_map import show_scatter_map

def show_charts_tab():
    st.info("📈 **Chart Elements**: Streamlit의 직관적인 내장 데이터 시각화 차트들입니다.")

    tab_basic_charts, tab_geo_charts = st.tabs([
        "📊 선형 / 막대 / 영역 차트",
        "🗺️ 산점도 & 지도 (Map)",
    ])

    with tab_basic_charts:
        show_line_bar_area()

    with tab_geo_charts:
        show_scatter_map()

