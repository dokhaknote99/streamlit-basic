import streamlit as st
from components.chat.chat_basics import show_chat_basics

def show_chat_tab():
    st.info("💬 **Chat Elements**: 대화형 인터페이스를 만드는 채팅 메시지 버블과 입력창입니다.")

    tab_chat = st.tabs(["💬 챗 메시지 & 입력"])
    with tab_chat[0]:
        show_chat_basics()

