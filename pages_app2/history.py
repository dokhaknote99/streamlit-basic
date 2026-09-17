import pandas as pd
import streamlit as st
from utils.db import (
    get_user_sessions,
    load_session_messages,
    delete_session,
)

user_id = st.session_state.get("user_id", "guest")

st.title("📜 과거 채팅 내역 뷰어")
st.caption(f"**{user_id}** 님의 대화 세션 기록을 조회하고 관리합니다. (최대 10개 보관, 세션당 최대 100회)")

# 1. 사용자의 대화 세션 목록 조회
sessions = get_user_sessions(user_id)

with st.sidebar:
    st.header("🗂️ 대화 세션 목록")

    if not sessions:
        st.info("저장된 대화 내역이 없습니다.")
        st.stop()

    search_kw = st.text_input("🔍 세션 제목 검색", placeholder="검색어 입력...")

    # 검색 필터링
    filtered_sessions = [s for s in sessions if search_kw.lower() in s[1].lower()] if search_kw else sessions

    if not filtered_sessions:
        st.warning("일치하는 대화 세션이 없습니다.")
        st.stop()

    session_map = {s[0]: f"{s[1]} ({s[3]}개 메시지)" for s in filtered_sessions}

    selected_sid = st.radio(
        label="조회할 대화를 선택하세요",
        options=list(session_map.keys()),
        format_func=lambda sid: session_map[sid],
    )

    st.divider()
    if st.button("🗑️ 선택한 대화 세션 삭제", use_container_width=True):
        delete_session(selected_sid)
        st.rerun()

# 2. 선택된 대화 세션 상세 정보 및 메시지
selected_session_info = next((s for s in sessions if s[0] == selected_sid), None)
msgs = load_session_messages(selected_sid)
df_msgs = pd.DataFrame(msgs)

# 상단 요약 지표 카드
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.metric("대화 제목", selected_session_info[1])
with m_col2:
    st.metric("생성 일시", selected_session_info[2][:19])
with m_col3:
    st.metric("총 메시지 수", f"{len(df_msgs)}개")

st.divider()

# 대화형 뷰 vs 데이터 테이블 뷰 분리
tab_chat, tab_table = st.tabs(["💬 대화형 메시지 뷰", "📊 데이터 테이블 뷰"])

with tab_chat:
    if df_msgs.empty:
        st.info("이 대화 세션에는 기록된 메시지가 없습니다.")
    else:
        for _, row in df_msgs.iterrows():
            with st.chat_message(row["role"]):
                st.write(row["content"])
                st.caption(f"🕒 {row['created_at']}")

        # 대화 텍스트 파일 다운로드
        chat_text = "\n\n".join([f"[{r['role'].upper()}] ({r['created_at']})\n{r['content']}" for _, r in df_msgs.iterrows()])
        st.download_button(
            label="📥 대화 내역 텍스트 다운로드 (.txt)",
            data=chat_text,
            file_name=f"{selected_session_info[1]}_대화기록.txt",
            mime="text/plain",
        )

with tab_table:
    if not df_msgs.empty:
        st.dataframe(df_msgs, width="stretch")
        csv_data = df_msgs.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 CSV 파일로 다운로드 (.csv)",
            data=csv_data,
            file_name=f"{selected_session_info[1]}_대화기록.csv",
            mime="text/csv",
        )
    else:
        st.info("테이블로 표시할 메시지가 없습니다.")
