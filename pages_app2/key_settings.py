import streamlit as st
from utils.ui_theme import apply_custom_theme, page_header

apply_custom_theme()

current_key = st.session_state.get("openai_api_key", "")

page_header(
    "🔑",
    "API Key 관리",
    "OpenAI API Key를 등록하면 채팅을 시작할 수 있어요.",
    chips=[("등록됨", "green")] if current_key else [("미등록", "amber")],
)

col_main, col_side = st.columns([1.5, 1], gap="medium")

with col_main:
    with st.container(border=True, key="card_key_form"):
        img_col, form_col = st.columns([1, 1.7], gap="medium", vertical_alignment="center")
        with img_col:
            st.image("assets/security_key.jpg", width="stretch")
        with form_col:
            if current_key:
                st.markdown("#### 등록 완료")
                st.caption("Key는 브라우저 세션 메모리에만 보관됩니다.")
                st.code(f"sk-...{current_key[-4:]}", language=None)

                btn_chat, btn_del = st.columns(2)
                with btn_chat:
                    if st.button("채팅 시작", icon=":material/chat:", width="stretch", type="primary"):
                        st.switch_page("pages_app2/chat.py")
                with btn_del:
                    if st.button("Key 삭제", icon=":material/delete:", width="stretch"):
                        st.session_state.pop("openai_api_key", None)
                        st.rerun()
            else:
                st.markdown("#### Key 등록")
                st.caption("OpenAI 플랫폼에서 발급받은 비밀 키를 입력하세요.")
                new_key = st.text_input(
                    "OpenAI API Key",
                    type="password",
                    placeholder="sk-...",
                    icon=":material/key:",
                    label_visibility="collapsed",
                )
                if st.button("Key 등록하기", icon=":material/check:", width="stretch", type="primary"):
                    if new_key.strip():
                        st.session_state["openai_api_key"] = new_key.strip()
                        st.rerun()
                    else:
                        st.warning("유효한 API Key를 입력해주세요.")

with col_side:
    with st.container(border=True, key="card_key_notes"):
        st.markdown("#### 보안 안내")
        st.markdown(
            """
- **DB 미저장** — API Key는 데이터베이스나 서버 파일에 저장되지 않습니다.
- **세션 휘발성** — 브라우저 탭 세션 메모리에만 상주하며 창을 닫으면 파기됩니다.
- **공용 PC 주의** — 사용 후 반드시 로그아웃 또는 Key 삭제를 진행하세요.
            """
        )
        st.link_button(
            "OpenAI Platform에서 키 발급받기",
            "https://platform.openai.com/api-keys",
            icon=":material/open_in_new:",
            width="stretch",
        )
