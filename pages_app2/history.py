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

st.title("📜 대화 내역")

sessions = get_user_sessions(user_id)

if not sessions:
    st.info("저장된 대화 내역이 없습니다.")
    st.stop()

# 1. 사이드바: 세션 선택 및 삭제
with st.sidebar:
    st.subheader("대화 목록")
    session_map = {s[0]: s[1] for s in sessions}

    selected_sid = st.radio(
        label="대화 선택",
        options=list(session_map.keys()),
        format_func=lambda sid: session_map[sid],
    )

    st.divider()
    if st.button("선택한 대화 삭제", use_container_width=True):
        delete_session(selected_sid)
        st.rerun()

# 2. 메인: 선택된 세션 상세
selected_session_info = next((s for s in sessions if s[0] == selected_sid), None)
msgs = load_session_messages(selected_sid)
df_msgs = pd.DataFrame(msgs)

st.subheader(selected_session_info[1])
st.caption(f"생성 일시: {selected_session_info[2]}")

tab_chat, tab_table = st.tabs(["대화 내용", "데이터 테이블"])

with tab_chat:
    if df_msgs.empty:
        st.info("저장된 메시지가 없습니다.")
    else:
        for _, row in df_msgs.iterrows():
            with st.chat_message(row["role"]):
                st.write(row["content"])
                st.caption(f"🕒 {row['created_at']}")

        chat_text = "\n\n".join([f"[{r['role'].upper()}] ({r['created_at']})\n{r['content']}" for _, r in df_msgs.iterrows()])
        st.download_button(
            label="텍스트 다운로드 (.txt)",
            data=chat_text,
            file_name=f"{selected_session_info[1]}_대화기록.txt",
            mime="text/plain",
        )

with tab_table:
    if not df_msgs.empty:
        st.dataframe(df_msgs, width="stretch")
        csv_data = df_msgs.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="CSV 다운로드 (.csv)",
            data=csv_data,
            file_name=f"{selected_session_info[1]}_대화기록.csv",
            mime="text/csv",
        )
    else:
        st.info("표시할 메시지가 없습니다.")
