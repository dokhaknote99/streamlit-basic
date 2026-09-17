import streamlit as st
from utils.ui_theme import apply_custom_theme

apply_custom_theme()

st.title("🔑 OpenAI API Key 관리 센터")
st.caption("안전한 AI 챗봇 대화를 위해 본인의 OpenAI API Key를 등록하고 메모리 상태를 관리합니다.")

# 1. 필수 보안 정책 및 취약점 안내 카드 (그리드 레이아웃)
st.markdown("### 🛡️ 보안 안전 원칙 및 가이드라인")
sec_col1, sec_col2 = st.columns(2)

with sec_col1:
    st.markdown(
        """
        <div class="glass-card">
            <h4 style="margin-top:0; color:#4f46e5;">🚫 1. 데이터베이스(DB) Zero-Storage</h4>
            <p style="font-size:0.9rem; color:gray; margin-bottom:0;">
                입력하신 API Key는 데이터베이스(DB)나 서버 디스크 파일에 <strong>절대 저장되지 않습니다</strong>.
                DB 테이블에는 사용자 대화 텍스트만 보관됩니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="glass-card">
            <h4 style="margin-top:0; color:#4f46e5;">💻 3. 공용 PC 안전 수칙</h4>
            <p style="font-size:0.9rem; color:gray; margin-bottom:0;">
                학교, 카페, PC방 등 공용 환경에서는 브라우저 탭을 닫기 전 반드시 <strong>[API Key 삭제]</strong> 또는 <strong>[로그아웃]</strong>을 진행해 주세요.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with sec_col2:
    st.markdown(
        """
        <div class="glass-card">
            <h4 style="margin-top:0; color:#4f46e5;">💨 2. 브라우저 세션 휘발성 메모리 보관</h4>
            <p style="font-size:0.9rem; color:gray; margin-bottom:0;">
                API Key는 오직 브라우저 세션 메모리(<code>st.session_state</code>)에만 일시적으로 상주하며, 탭을 닫거나 새로고침 시 즉시 영구 파기됩니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="glass-card">
            <h4 style="margin-top:0; color:#4f46e5;">🔒 4. 공식 OpenAI 엔드포인트 직결</h4>
            <p style="font-size:0.9rem; color:gray; margin-bottom:0;">
                중간 프록시 서버 없이 브라우저 환경에서 OpenAI의 공식 SSL 암호화 API 엔드포인트로만 다이렉트 통신합니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
st.markdown("### ⚙️ API Key 설정 및 상태")

# 2. Key 등록 및 상태 제어
current_key = st.session_state.get("openai_api_key", "")

if current_key:
    # 키가 이미 등록된 경우: 세련된 활성화 상태 카드
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div style="font-size: 1.15rem; font-weight: 700; color: #10b981;">
                    ✅ API Key가 세션 메모리에 안전하게 활성화되어 있습니다
                </div>
                <span class="status-chip status-active">🟢 사용 가능</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        masked_key = f"sk-{'•' * 28}{current_key[-4:]}"
        st.code(masked_key, language="text")
        st.caption("ℹ️ 현재 활성화된 세션에만 임시 보관 중입니다. 브라우저를 닫으면 자동으로 소멸합니다.")

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        act_col1, act_col2 = st.columns([1, 1])

        with act_col1:
            if st.button("💬 지금 챗봇과 대화하러 가기", use_container_width=True, type="primary"):
                st.switch_page("pages_app2/chat.py")

        with act_col2:
            if st.button("🗑️ 등록된 API Key 즉시 파기 (메모리 삭제)", use_container_width=True):
                st.session_state.pop("openai_api_key", None)
                st.rerun()

else:
    # 키가 등록되지 않은 경우: 깔끔한 입력 폼 카드
    with st.container(border=True):
        st.markdown("#### 🔑 신규 OpenAI API Key 등록")
        st.caption("챗봇과 대화하기 위해 유효한 API Key를 입력해주세요. 입력된 키는 DB에 저장되지 않습니다.")

        new_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-proj-...",
            help="OpenAI 플랫폼(platform.openai.com) 대시보드에서 발급받은 비밀 키를 입력하세요.",
        )

        st.caption("💡 아직 API Key가 없으신가요? [OpenAI Platform 바로가기 ↗](https://platform.openai.com/api-keys)")

        if st.button("🔑 API Key 세션에 등록하기", use_container_width=True, type="primary"):
            if new_key.strip():
                st.session_state["openai_api_key"] = new_key.strip()
                st.success("API Key가 현재 브라우저 세션에 안전하게 등록되었습니다!")
                st.rerun()
            else:
                st.warning("유효한 API Key를 입력해주세요.")
