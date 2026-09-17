import pandas as pd
import streamlit as st
from utils.db import (
    get_user_sessions,
    load_session_messages,
    delete_session,
)
from utils.ui_theme import apply_custom_theme, page_header, empty_state, session_labels

apply_custom_theme()

ASSISTANT_AVATAR = "assets/logo.jpg"

user_id = st.session_state.get("user_id", "guest")

sessions = get_user_sessions(user_id)

if not sessions:
    page_header("📜", "대화 내역", "지난 대화를 다시 보고 텍스트나 CSV로 내보낼 수 있어요.")
    _, col_empty, _ = st.columns([1, 1.3, 1])
    with col_empty:
        with st.container(border=True, key="card_history_empty"):
            empty_state(
                "아직 저장된 대화가 없어요",
                "첫 대화를 시작하면 이곳에서 언제든 다시 확인하고 내보낼 수 있습니다.",
            )
            if st.button("지금 대화 시작하기", icon=":material/chat:", width="stretch", type="primary"):
                st.switch_page("pages_app2/chat.py")
    st.stop()

# 1. 사이드바: 대화 목록 탐색 및 세션 삭제
with st.sidebar:
    st.caption("대화 목록")
    label_map = session_labels(sessions)

    selected_sid = st.radio(
        label="조회할 대화 선택",
        options=list(label_map.keys()),
        format_func=lambda sid: label_map[sid],
        label_visibility="collapsed",
        width="stretch",
        key="session_list_history",
    )

    st.divider()
    if st.button("선택 대화 삭제", icon=":material/delete:", width="stretch"):
        delete_session(selected_sid)
        # 삭제된 세션이 위젯 선택값으로 남지 않도록 초기화
        st.session_state.pop("session_list_history", None)
        if st.session_state.get("current_session_id") == selected_sid:
            st.session_state.pop("current_session_id", None)
        st.rerun()

# 2. 메인: 선택된 세션 상세 헤더 및 데이터 뷰
selected_session_info = next((s for s in sessions if s[0] == selected_sid), None)
msgs = load_session_messages(selected_sid)
df_msgs = pd.DataFrame(msgs)

page_header(
    "📜",
    selected_session_info[1],
    chips=[
        (f"생성 {selected_session_info[2]}", "gray"),
        (f"메시지 {len(msgs)}개", ""),
    ],
)

tab_chat, tab_table = st.tabs(["💬 대화 내용", "📊 데이터 테이블"])

with tab_chat:
    if df_msgs.empty:
        st.info("저장된 메시지가 없습니다.")
    else:
        with st.container(height=480, border=True, key="card_history_chat"):
            for _, row in df_msgs.iterrows():
                avatar = ASSISTANT_AVATAR if row["role"] == "assistant" else None
                with st.chat_message(row["role"], avatar=avatar):
                    st.write(row["content"])
                    st.caption(f"🕒 {row['created_at']}")

        chat_text = "\n\n".join(
            [f"[{r['role'].upper()}] ({r['created_at']})\n{r['content']}" for _, r in df_msgs.iterrows()]
        )
        st.download_button(
            label="텍스트 파일 (.txt) 다운로드",
            icon=":material/download:",
            data=chat_text,
            file_name=f"{selected_session_info[1]}_대화기록.txt",
            mime="text/plain",
            type="primary",
        )

with tab_table:
    if not df_msgs.empty:
        st.dataframe(df_msgs, width="stretch", height=480)
        csv_data = df_msgs.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="CSV 파일 (.csv) 다운로드",
            icon=":material/download:",
            data=csv_data,
            file_name=f"{selected_session_info[1]}_대화기록.csv",
            mime="text/csv",
            type="primary",
        )
    else:
        st.info("표시할 메시지가 없습니다.")
