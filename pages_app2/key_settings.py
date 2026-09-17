import streamlit as st
from utils.ui_theme import apply_custom_theme

apply_custom_theme()

st.title("🔑 API Key 등록")

# 보안 안내 메시지
st.warning("""
**⚠️ 보안 주의사항 및 취약점 안내**
- **DB 미저장**: 입력하신 API Key는 데이터베이스나 디스크에 저장되지 않습니다.
- **세션 휘발성**: 브라우저 세션 메모리에만 일시 보관되며 창을 닫거나 로그아웃 시 즉시 삭제됩니다.
- **공용 PC 주의**: 공용 PC 사용 후 반드시 로그아웃 또는 키 삭제를 진행해주세요.
- **키 노출 방지**: 본인의 API Key가 타인에게 노출되지 않도록 주의해주세요.
""")

current_key = st.session_state.get("openai_api_key", "")

if current_key:
    with st.container(border=True):
        st.success(f"API Key 등록됨: `sk-...{current_key[-4:]}`")
        if st.button("🗑️ API Key 삭제", use_container_width=True):
            st.session_state.pop("openai_api_key", None)
            st.rerun()
else:
    with st.container(border=True):
        new_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
        )
        if st.button("등록하기", use_container_width=True, type="primary"):
            if new_key.strip():
                st.session_state["openai_api_key"] = new_key.strip()
                st.rerun()
            else:
                st.warning("유효한 API Key를 입력해주세요.")
