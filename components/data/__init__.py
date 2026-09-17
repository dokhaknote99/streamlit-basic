import streamlit as st
from components.data.dataframes import show_dataframes
from components.data.tables_metrics import show_tables_metrics
from components.data.json_data import show_json_data

def show_data_tab():
    st.info("📊 **Data Elements**: 표, 데이터프레임, KPI 지표 등 데이터를 직관적으로 표현하는 컴포넌트들입니다.")

    tab_df, tab_metric, tab_json = st.tabs([
        "📊 데이터프레임 & 에디터",
        "📈 KPI 지표 & 테이블",
        "🗂️ JSON 트리 뷰",
    ])

    with tab_df:
        show_dataframes()

    with tab_metric:
        show_tables_metrics()

    with tab_json:
        show_json_data()

