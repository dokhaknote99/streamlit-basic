import streamlit as st
from utils.ui_theme import apply_custom_theme

apply_custom_theme()

st.title("🔑 OpenAI API Key 관리")

current_key = st.session_state.get("openai_api_key", "")

_, col_center, _ = st.columns([1, 1.6, 1])

with col_center:
    st.image("assets/security_key.jpg", width="stretch")

    with st.container(border=True):
        if current_key:
            st.subheader("등록 완료")
            st.success(f"현재 등록된 Key: `sk-...{current_key[-4:]}`")
            st.caption("브라우저 메모리에 안전하게 등록되어 있습니다.")

            col_chat, col_del = st.columns(2)
            with col_chat:
                if st.button("💬 채팅 시작", use_container_width=True, type="primary"):
                    st.switch_page("pages_app2/chat.py")
            with col_del:
                if st.button("🗑️ Key 삭제", use_container_width=True):
                    st.session_state.pop("openai_api_key", None)
                    st.rerun()
        else:
            st.subheader("Key 등록")
            new_key = st.text_input(
                "OpenAI API Key 입력",
                type="password",
                placeholder="sk-...",
                help="OpenAI 플랫폼에서 발급받은 비밀 키를 입력하세요.",
            )
            if st.button("Key 등록하기", use_container_width=True, type="primary"):
                if new_key.strip():
                    st.session_state["openai_api_key"] = new_key.strip()
                    st.rerun()
                else:
                    st.warning("유효한 API Key를 입력해주세요.")

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.subheader("⚠️ 보안 안내")
        st.markdown("""
        - **DB 미저장**: API Key는 데이터베이스나 서버 파일에 일체 저장되지 않습니다.
        - **세션 휘발성**: 브라우저 탭 세션 메모리에만 상주하며 창을 닫으면 파기됩니다.
        - **공용 PC 주의**: 공용 PC 사용 후 반드시 로그아웃 또는 Key 삭제를 진행하세요.
        """)
        st.link_button("OpenAI Platform에서 키 발급받기 ↗", "https://platform.openai.com/api-keys", use_container_width=True)
