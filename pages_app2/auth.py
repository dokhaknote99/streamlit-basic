import streamlit as st
from utils.ui_theme import apply_custom_theme

apply_custom_theme()

current_user = st.session_state.get("user_id")

st.title("👤 계정")

if not current_user:
    with st.container(border=True):
        st.subheader("로그인")
        username_input = st.text_input(
            "사용자 ID",
            placeholder="아이디 또는 닉네임을 입력하세요",
        )

        if st.button("로그인", use_container_width=True, type="primary"):
            if username_input.strip():
                st.session_state["user_id"] = username_input.strip()
                st.rerun()
            else:
                st.warning("사용자 ID를 입력해주세요.")
else:
    with st.container(border=True):
        st.write(f"현재 **{current_user}** 님으로 로그인되어 있습니다.")
        key_status = "등록됨" if st.session_state.get("openai_api_key") else "미등록"
        st.write(f"API Key 상태: **{key_status}**")

        if st.button("로그아웃", use_container_width=True):
            st.session_state.pop("user_id", None)
            st.session_state.pop("openai_api_key", None)
            st.session_state.pop("current_session_id", None)
            st.rerun()
