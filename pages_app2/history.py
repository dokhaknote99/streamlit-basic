import pandas as pd
import streamlit as st
from utils.db import (
    get_user_sessions,
    load_session_messages,
    delete_session,
)
from utils.ui_theme import apply_custom_theme

apply_custom_theme()

user_id = st.session_state.get("user_id", "guest")

st.title("📜 대화 기록 보관소")
st.caption(f"**{user_id}** 님의 대화 기록을 타임라인 및 데이터 테이블로 조회하고 다운로드합니다.")

# 1. 사용자의 대화 세션 목록 조회
sessions = get_user_sessions(user_id)

if not sessions:
    st.markdown(
        """
        <div style="background: rgba(128, 128, 128, 0.05); border: 1px dashed rgba(128, 128, 128, 0.3); border-radius: 14px; padding: 40px; text-align: center; margin-top: 30px;">
            <div style="font-size: 2.8rem; margin-bottom: 8px;">📭</div>
            <h3 style="font-size: 1.3rem; font-weight: 700; margin-bottom: 8px;">저장된 대화 기록이 없습니다</h3>
            <p style="color: gray; font-size: 0.95rem; margin-bottom: 20px;">
                챗봇과 새로운 대화를 시작하면 이곳에 최대 10개의 세션 기록이 자동으로 보관됩니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    _, c_btn, _ = st.columns([1, 1, 1])
    with c_btn:
        if st.button("💬 지금 대화 시작하러 가기", use_container_width=True, type="primary"):
            st.switch_page("pages_app2/chat.py")
    st.stop()

# 2. 사이드바: 검색 및 세션 선택
with st.sidebar:
    st.markdown("### 🗂️ 세션 탐색 및 필터")
    search_kw = st.text_input("🔍 세션 제목 검색", placeholder="검색어 입력...")

    # 검색 필터링
    filtered_sessions = [s for s in sessions if search_kw.lower() in s[1].lower()] if search_kw else sessions

    if not filtered_sessions:
        st.warning("검색 조건과 일치하는 대화 세션이 없습니다.")
        st.stop()

    session_map = {s[0]: f"{s[1]} ({s[3]}건)" for s in filtered_sessions}

    selected_sid = st.radio(
        label="조회할 대화 세션을 선택하세요",
        options=list(session_map.keys()),
        format_func=lambda sid: session_map[sid],
    )

    st.divider()
    if st.button("🗑️ 선택 세션 삭제", use_container_width=True):
        delete_session(selected_sid)
        st.rerun()

# 3. 메인: 선택된 세션 정보 및 상단 지표 카드
selected_session_info = next((s for s in sessions if s[0] == selected_sid), None)
msgs = load_session_messages(selected_sid)
df_msgs = pd.DataFrame(msgs)

# 4개 지표 카드
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.metric("📁 보관 세션 현황", f"{len(sessions)} / 10개")
with m_col2:
    st.metric("💬 선택 세션 메시지", f"{len(df_msgs)} / 200개")
with m_col3:
    created_time = selected_session_info[2][:16] if selected_session_info else "-"
    st.metric("🕒 세션 생성 일시", created_time)
with m_col4:
    st.metric("👤 소유 계정", user_id)

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# 4. 대화형 뷰 vs 데이터 테이블 뷰
tab_chat, tab_table = st.tabs(["💬 대화 타임라인 뷰", "📊 데이터 테이블 뷰"])

with tab_chat:
    if df_msgs.empty:
        st.info("이 대화 세션에는 기록된 메시지가 없습니다.")
    else:
        for _, row in df_msgs.iterrows():
            with st.chat_message(row["role"]):
                st.write(row["content"])
                st.caption(f"🕒 기록 시각: {row['created_at']}")

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        # 텍스트 다운로드 바
        chat_text = "\n\n".join([f"[{r['role'].upper()}] ({r['created_at']})\n{r['content']}" for _, r in df_msgs.iterrows()])
        st.download_button(
            label="📥 대화 내역 텍스트 다운로드 (.txt)",
            data=chat_text,
            file_name=f"{selected_session_info[1]}_대화기록.txt",
            mime="text/plain",
            type="primary",
        )

with tab_table:
    if not df_msgs.empty:
        st.dataframe(
            df_msgs,
            width="stretch",
            column_config={
                "role": st.column_config.TextColumn("역할 (Role)", width="small"),
                "content": st.column_config.TextColumn("대화 내용 (Content)", width="large"),
                "created_at": st.column_config.DatetimeColumn("기록 일시 (Timestamp)", format="YYYY-MM-DD HH:mm:ss"),
            },
        )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        csv_data = df_msgs.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 CSV 파일로 내보내기 (.csv)",
            data=csv_data,
            file_name=f"{selected_session_info[1]}_대화기록.csv",
            mime="text/csv",
            type="primary",
        )
    else:
        st.info("테이블로 표시할 메시지가 없습니다.")
