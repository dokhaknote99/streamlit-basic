import streamlit as st

st.title("👤 사용자 로그인")
st.caption("사용자 ID를 입력하여 로그인하면, 본인만의 대화 세션과 히스토리를 독립적으로 관리할 수 있습니다.")

current_user = st.session_state.get("user_id")

if current_user:
    st.success(f"현재 **{current_user}** 님으로 로그인되어 있습니다.")
    st.info("좌측 사이드바 메뉴를 통해 챗봇 대화나 API Key 등록 페이지로 이동하실 수 있습니다.")

    if st.button("🚪 로그아웃", use_container_width=True):
        st.session_state.pop("user_id", None)
        st.session_state.pop("openai_api_key", None)
        st.session_state.pop("current_session_id", None)
        st.rerun()
else:
    with st.container(border=True):
        st.subheader("로그인")
        username_input = st.text_input("사용자 ID (아이디 또는 닉네임 입력)", placeholder="예: user123, alex")

        if st.button("로그인하기", use_container_width=True):
            if username_input.strip():
                st.session_state["user_id"] = username_input.strip()
                st.rerun()
            else:
                st.warning("사용자 ID를 입력해주세요.")
