import streamlit as st

st.title("🔑 OpenAI API Key 등록")
st.caption("챗봇과 대화하기 위해 필요한 OpenAI API Key를 등록하고 관리하는 페이지입니다.")

# 1. 보안 취약점 안내 메시지 (필수 요구사항)
st.warning("""
### ⚠️ 보안 주의사항 및 취약점 안내
1. **DB 미저장 원칙**: 입력하신 API Key는 데이터베이스(DB)나 서버 디스크에 **절대 저장되지 않습니다**.
2. **세션 휘발성**: API Key는 브라우저를 사용하는 동안 현재 세션 메모리(`st.session_state`)에만 일시 보관되며, 브라우저를 닫거나 로그아웃 시 즉시 영구 파기됩니다.
3. **공용 PC 주의**: PC방이나 공용 컴퓨터에서 이용하시는 경우, 사용을 마친 후 반드시 **[로그아웃]** 또는 **[API Key 삭제]**를 눌러 키가 남지 않도록 주의해 주세요.
4. **키 노출 방지**: 본인의 API Key가 타인에게 노출되지 않도록 각별히 관리해 주시기 바랍니다.
""")

st.divider()

# 2. Key 등록 폼
current_key = st.session_state.get("openai_api_key", "")

if current_key:
    # 키가 이미 등록된 경우
    st.success("✅ OpenAI API Key가 현재 세션에 안전하게 등록되어 있습니다.")
    st.info(f"등록된 Key 상태: `sk-...{current_key[-4:]}` (메모리 보관 중)")

    if st.button("🗑️ 등록된 API Key 삭제 (메모리에서 파기)", use_container_width=True):
        st.session_state.pop("openai_api_key", None)
        st.rerun()
else:
    # 키가 등록되지 않은 경우
    st.info("💡 챗봇을 이용하시려면 아래에 유효한 OpenAI API Key를 입력해주세요.")
    with st.container(border=True):
        new_key = st.text_input(
            "OpenAI API Key 입력",
            type="password",
            placeholder="sk-proj-...",
            help="OpenAI 플랫폼(platform.openai.com)에서 발급받은 API 키를 입력하세요.",
        )

        if st.button("🔑 API Key 등록하기", use_container_width=True):
            if new_key.strip():
                st.session_state["openai_api_key"] = new_key.strip()
                st.success("API Key가 현재 브라우저 세션에 안전하게 등록되었습니다! 이제 챗봇 대화를 이용하실 수 있습니다.")
                st.rerun()
            else:
                st.warning("유효한 API Key를 입력해주세요.")
