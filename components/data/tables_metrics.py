import streamlit as st
import pandas as pd

def show_tables_metrics():
    st.header("📈 테이블 및 지표 카드 (st.table & st.metric)")

    # 1. 지표 카드 (st.metric)
    st.subheader("1. KPI 지표 카드 (st.metric)")
    st.caption("현재 값(value)과 이전 대비 증감(delta)을 직관적인 화살표와 색상으로 표시합니다.")

    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric(label="월 매출액", value="₩125,000,000", delta="+12.5%")
    with m_col2:
        st.metric(label="이탈률", value="2.4%", delta="-0.8%", delta_color="inverse")
    with m_col3:
        st.metric(label="활성 사용자 수", value="45,210명", delta="0% (변동없음)", delta_color="off")

    st.divider()

    # 2. 정적 테이블 (st.table)
    st.subheader("2. 정적 테이블 (st.table)")
    st.caption("인터랙티브 기능 없이 모든 행과 열이 펼쳐져 고정 표시되는 테이블입니다.")
    summary_data = {
        "구분": ["목표", "현재", "달성률"],
        "매출": ["1억 원", "1.25억 원", "125%"],
        "신규가입": ["5,000명", "4,800명", "96%"],
    }
    st.table(pd.DataFrame(summary_data))

