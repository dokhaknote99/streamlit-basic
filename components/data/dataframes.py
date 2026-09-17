import streamlit as st
import pandas as pd

def show_dataframes():
    st.header("📊 데이터프레임 (st.dataframe & st.data_editor)")

    # 샘플 데이터 생성
    data = {
        "제품명": ["스마트폰", "노트북", "무선이어폰", "스마트워치", "태블릿"],
        "카테고리": ["전자제품", "컴퓨터", "음향", "웨어러블", "컴퓨터"],
        "가격(원)": [1200000, 1800000, 250000, 350000, 800000],
        "재고": [45, 12, 80, 30, 20],
        "판매중": [True, True, True, False, True],
    }
    df = pd.DataFrame(data)

    # 1. 인터랙티브 데이터프레임
    st.subheader("1. 인터랙티브 데이터프레임 (st.dataframe)")
    st.caption("열 정렬, 필터, 크기 조절, 인덱스 숨김(hide_index=True)을 지원합니다.")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # 2. 직접 수정 가능한 데이터 에디터
    st.subheader("2. 데이터 에디터 (st.data_editor)")
    st.caption("스프레드시트처럼 브라우저에서 바로 셀을 더블클릭해 값을 수정하거나 행을 추가(num_rows='dynamic')할 수 있습니다.")
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    st.write("👉 수정된 데이터 실시간 반영:")
    st.write(edited_df)

