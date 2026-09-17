import streamlit as st

def show_chat_basics():
    st.header("💬 채팅 인터페이스 (st.chat_message & st.chat_input)")
    st.caption("ChatGPT와 같은 대화형 LLM 챗봇 UI를 손쉽게 구축할 수 있는 전용 컴포넌트입니다.")

    # 1. 챗봇 메시지 버블 (st.chat_message)
    st.subheader("1. 메시지 버블 (st.chat_message)")

    with st.chat_message("user"):
        st.write("사용자 메시지: Streamlit에서 챗봇 UI는 어떻게 만드나요?")

    with st.chat_message("assistant"):
        st.write("AI 어시스턴트: `st.chat_message`와 `st.chat_input`을 결합하면 간단하게 대화형 챗봇 화면을 완성할 수 있습니다!")

    with st.chat_message("custom", avatar="🤖"):
        st.write("커스텀 아바타: 이모지나 커스텀 이미지 URL을 아바타로 지정할 수도 있습니다.")

    st.divider()

    # 2. 채팅 전용 입력창 (st.chat_input)
    st.subheader("2. 채팅 입력창 (st.chat_input)")
    st.caption("화면 하단에 입력 바가 고정되며, 엔터를 치면 값이 반환됩니다.")
    prompt = st.chat_input("질문할 내용을 입력해 보세요 (Enter를 치면 상단에 반응)")
    if prompt:
        st.info(f"방금 입력된 메시지: {prompt}")

