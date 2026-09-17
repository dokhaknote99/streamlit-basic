import streamlit as st
from components.write_magic.write_basics import show_write_basics
from components.write_magic.stream_magic import show_stream_magic

def show_write_magic_tab():
    st.info("✍️ **Write and Magic**: Streamlit의 가장 기본적인 출력 방식들을 확인해보세요.")

    tab_basics, tab_magic = st.tabs([
        "📄 st.write 기본 및 다양한 타입",
        "✨ 스트리밍 & Magic 기능",
    ])

    with tab_basics:
        show_write_basics()

    with tab_magic:
        show_stream_magic()

