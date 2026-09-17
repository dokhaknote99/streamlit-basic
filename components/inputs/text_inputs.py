import streamlit as st

def show_text_inputs():
    st.subheader("1. 기본 입력과 초기값 (value)")
    val = st.text_input(label="이름", value="홍길동")
    st.write("👉 현재 입력값:", val)

    st.subheader("2. 안내 문구(placeholder) 및 도움말(help)")
    hint_val = st.text_input(
        label="이메일",
        placeholder="user@example.com",
        help="마우스를 올리면 물음표 아이콘과 함께 안내 툴팁이 뜹니다.",
    )
    st.write("👉 현재 입력값:", hint_val)

    st.subheader("3. 비밀번호 입력 (type='password')")
    pwd = st.text_input(label="비밀번호", type="password")
    st.write("👉 입력된 실제 비밀번호:", pwd)

    st.subheader("4. 최대 입력 글자 수 제한 (max_chars)")
    code = st.text_input(label="인증번호 (최대 6자리)", max_chars=6)
    st.write("👉 현재 입력값:", code)

    st.subheader("5. 라벨 표시 옵션 (label_visibility)")
    st.write("- `visible`: 기본값 (라벨 정상 표시)")
    st.write("- `hidden`: 라벨 텍스트는 숨기되 상단 공간 유지")
    st.write("- `collapsed`: 라벨 텍스트와 상단 공간을 모두 제거 (검색창 스타일)")

    v1 = st.text_input("라벨 표시 (visible)", label_visibility="visible")
    v2 = st.text_input("라벨 공간 유지 숨김 (hidden)", placeholder="hidden: 라벨 공간 유지", label_visibility="hidden")
    v3 = st.text_input("라벨 및 공간 제거 (collapsed)", placeholder="collapsed: 검색창처럼 공간 제거", label_visibility="collapsed")

    st.subheader("6. 비활성화 입력창 (disabled=True)")
    st.text_input("수정 불가 항목", value="사용자가 수정할 수 없는 읽기 전용 상태입니다.", disabled=True)

    st.subheader("7. 여러 줄 텍스트 입력 (st.text_area)")
    area_text = st.text_area(
        label="자기소개 또는 메모",
        value="첫 번째 줄\n두 번째 줄",
        height=120,
        max_chars=200,
        placeholder="여러 줄의 내용을 자유롭게 입력하세요.",
    )
    st.write(f"👉 입력 글자 수: {len(area_text)} / 200자")
    st.write("👉 입력 내용 미리보기:")
    st.text(area_text)

    st.subheader("8. 채팅 입력창 (st.chat_input)")
    st.caption("화면 맨 아래쪽에 고정되는 입력창입니다.")
    chat_msg = st.chat_input("메시지를 입력 후 엔터를 눌러보세요")
    st.write("👉 전송된 메시지:", chat_msg)

