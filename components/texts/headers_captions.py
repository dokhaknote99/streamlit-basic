import streamlit as st

def show_headers_captions():
    st.header("🔤 제목, 캡션 및 구분선 (Title, Headers, Captions, Dividers)")

    # 1. 제목 계층 구조
    st.title("st.title (최상위 대제목)")
    st.header("st.header (주요 섹션 제목)")
    st.subheader("st.subheader (소단락 제목)")

    # 2. 일반 텍스트 및 캡션
    st.text("st.text: 서식 없는 고정폭 일반 텍스트입니다.")
    st.caption("st.caption: 각주나 보충 설명을 위한 작고 옅은 텍스트입니다.")

    # 3. 구분선 (st.divider)
    st.write("아래는 st.divider()로 생성된 가로 구분선입니다:")
    st.divider()
    st.write("구분선 아래의 텍스트입니다.")

