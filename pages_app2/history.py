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

st.title("📜 과거 대화 내역")

sessions = get_user_sessions(user_id)

if not sessions:
    st.info("저장된 대화 내역이 없습니다.")
    st.stop()

# 1. 사이드바: 오직 대화 목록 탐색 및 세션 삭제 옵션만 배치
with st.sidebar:
    st.subheader("📜 대화 목록")
    session_map = {s[0]: s[1] for s in sessions}

    selected_sid = st.radio(
        label="조회할 대화 선택",
        options=list(session_map.keys()),
        format_func=lambda sid: session_map[sid],
    )

    st.divider()
    if st.button("🗑️ 선택 대화 삭제", use_container_width=True):
        delete_session(selected_sid)
        st.rerun()

# 2. 메인: 선택된 세션 상세 헤더 및 데이터 뷰
selected_session_info = next((s for s in sessions if s[0] == selected_sid), None)
msgs = load_session_messages(selected_sid)
df_msgs = pd.DataFrame(msgs)

col_head, col_meta = st.columns([3, 1])
with col_head:
    st.subheader(f"대화 제목: {selected_session_info[1]}")
with col_meta:
    st.caption(f"생성 일시:\n{selected_session_info[2]}")

tab_chat, tab_table = st.tabs(["💬 대화 내용 뷰", "📊 데이터 테이블 뷰"])

with tab_chat:
    if df_msgs.empty:
        st.info("저장된 메시지가 없습니다.")
    else:
        for _, row in df_msgs.iterrows():
            with st.chat_message(row["role"]):
                st.write(row["content"])
                st.caption(f"🕒 {row['created_at']}")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        chat_text = "\n\n".join([f"[{r['role'].upper()}] ({r['created_at']})\n{r['content']}" for _, r in df_msgs.iterrows()])
        st.download_button(
            label="📥 텍스트 파일 (.txt) 다운로드",
            data=chat_text,
            file_name=f"{selected_session_info[1]}_대화기록.txt",
            mime="text/plain",
            type="primary",
        )

with tab_table:
    if not df_msgs.empty:
        st.dataframe(df_msgs, width="stretch")
        csv_data = df_msgs.to_csv(index=False).encode("utf-8-sig")
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        st.download_button(
            label="📥 CSV 파일 (.csv) 다운로드",
            data=csv_data,
            file_name=f"{selected_session_info[1]}_대화기록.csv",
            mime="text/csv",
            type="primary",
        )
    else:
        st.info("표시할 메시지가 없습니다.")
