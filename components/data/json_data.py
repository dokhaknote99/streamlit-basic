import streamlit as st

def show_json_data():
    st.header("🗂️ JSON 데이터 뷰어 (st.json)")
    st.caption("계층 구조를 가진 딕셔너리나 JSON 데이터를 접기/펼치기가 가능한 트리 뷰로 표시합니다.")

    api_response = {
        "status": "success",
        "code": 200,
        "data": {
            "user": {
                "id": "usr_98765",
                "name": "홍길동",
                "profile": {
                    "age": 28,
                    "location": "Seoul, Korea",
                    "skills": ["Python", "Streamlit", "SQL"],
                },
            },
            "preferences": {
                "theme": "dark",
                "notifications": True,
            },
        },
    }

    st.subheader("1. 기본 JSON 뷰어")
    st.json(api_response)

    st.subheader("2. 초기 접힘 상태 지정 (expanded=False)")
    st.json(api_response, expanded=False)

