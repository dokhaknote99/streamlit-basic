import streamlit as st

def show_markdown_formatting():
    st.header("📝 마크다운 서식 & 컬러링 (st.markdown)")

    # 1. 텍스트 강조 서식
    st.subheader("1. 기본 마크다운 스타일")
    st.markdown("""
    - **굵은 글씨 (Bold)**
    - *기울임 (Italic)*
    - ~~취소선 (Strikethrough)~~
    - [Streamlit 공식 홈페이지 링크](https://streamlit.io)
    - 리스트 항목 1
    - 리스트 항목 2
    """)

    # 2. Streamlit 고유 텍스트 컬러링 문법
    st.subheader("2. 텍스트 및 배경 색상 적용")
    st.markdown("Streamlit 고유의 컬러 태그 `:color[...]` 및 `:color-background[...]` 문법:")
    st.markdown("""
    - :red[빨간색 텍스트], :blue[파란색 텍스트], :green[초록색 텍스트], :orange[주황색 텍스트], :violet[보라색 텍스트]
    - :red-background[빨간색 배경], :blue-background[파란색 배경], :green-background[초록색 배경]
    """)

    # 3. 이모지 단축어
    st.subheader("3. 이모지 단축어 지원")
    st.markdown("단축어를 사용한 이모지: :rocket: `:rocket:`, :star: `:star:`, :heart: `:heart:`, :fire: `:fire:`")

