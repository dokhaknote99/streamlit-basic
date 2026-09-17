import time
import streamlit as st

def show_stream_magic():
    st.header("✨ st.write_stream & Magic 명령어")

    # 1. 스트리밍 출력 (st.write_stream)
    st.subheader("1. 텍스트 스트리밍 (st.write_stream)")
    st.caption("LLM 챗봇처럼 글자가 한 글자씩 타이핑되듯 나타나는 효과를 냅니다.")

    def stream_sample():
        sample_text = "안녕하세요! Streamlit의 write_stream 기능을 사용하여 실시간 타이핑 효과를 체험하고 있습니다."
        for word in sample_text.split(" "):
            yield word + " "
            time.sleep(0.08)

    if st.button("텍스트 스트리밍 재생"):
        st.write_stream(stream_sample)

    st.divider()

    # 2. 매직(Magic) 기능 소개
    st.subheader("2. Streamlit Magic (코드 단독 작성만으로 자동 출력)")
    st.caption("Streamlit에서는 st.write() 없이도 변수나 문자열을 줄에 적기만 하면 화면에 바로 출력됩니다.")

    st.code("""
# 코드 작성 예시:
'''
# 이것은 Magic 타이틀입니다!
마크다운 문법도 바로 적용됩니다.
'''
x = 42
x  # 42가 화면에 바로 표시됩니다!
    """, language="python")

    # 실제 매직 동작 예시
    """
    이 영역은 `st.write()`를 호출하지 않고 **독스트링/문자열 자체**만으로 출력된 Magic 예시입니다.
    """

