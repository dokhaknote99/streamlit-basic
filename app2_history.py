import sqlite3
import pandas as pd
import streamlit as st

st.title("📜 과거 채팅 내역 뷰어")
st.caption("SQLite(chat_history.db)에 저장된 대화 세션과 메시지 기록을 조회하고 관리합니다.")

DB_FILE = "chat_history.db"

# 1. SQLite DB 조회 및 삭제 함수
def get_sessions():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.id, s.title, s.created_at, COUNT(m.id) as msg_count
        FROM sessions s
        LEFT JOIN messages m ON s.id = m.session_id
        GROUP BY s.id
        ORDER BY s.created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_session_messages(session_id):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query(
        "SELECT id, role, content, file_name, created_at FROM messages WHERE session_id = ? ORDER BY id ASC",
        conn,
        params=(session_id,),
    )
    conn.close()
    return df

def delete_session(session_id):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()

# 2. 사이드바: 대화 세션 목록 및 검색
sessions = get_sessions()

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

# 3. 메인 화면: 선택된 대화 세션 상세 표시
selected_session_info = next((s for s in sessions if s[0] == selected_sid), None)
df_msgs = get_session_messages(selected_sid)

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
                if row["file_name"]:
                    st.caption(f"📎 첨부파일: {row['file_name']}")
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
    st.dataframe(df_msgs, width="stretch")

    # CSV 파일 다운로드
    csv_data = df_msgs.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="📥 CSV 파일로 다운로드 (.csv)",
        data=csv_data,
        file_name=f"{selected_session_info[1]}_대화기록.csv",
        mime="text/csv",
    )
