import streamlit as st
from components.texts.headers_captions import show_headers_captions
from components.texts.markdown_formatting import show_markdown_formatting
from components.texts.code_latex import show_code_latex

def show_texts_tab():
    st.info("📝 **Text Elements**: 텍스트를 화면에 구조화하고 아름답게 표현하는 방법들을 확인해보세요.")

    tab_headers, tab_markdown, tab_code = st.tabs([
        "🔤 제목 및 캡션",
        "🎨 마크다운 & 컬러 서식",
        "💻 코드 및 LaTeX 수식",
    ])

    with tab_headers:
        show_headers_captions()

    with tab_markdown:
        show_markdown_formatting()

    with tab_code:
        show_code_latex()

