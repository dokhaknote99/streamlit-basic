import streamlit as st
from components.inputs.text_inputs import show_text_inputs
from components.inputs.numbers_sliders import show_numbers_sliders
from components.inputs.selections import show_selections
from components.inputs.date_time_extras import show_date_time_extras

def show_inputs_tab():
    st.info("💡 **입력 위젯 카테고리**: 아래 하위 탭을 통해 다양한 사용자 입력 위젯들을 확인해보세요.")

    tab_text, tab_number, tab_selection, tab_datetime = st.tabs([
        "🔤 텍스트 입력",
        "🔢 숫자 & 슬라이더",
        "🔘 선택 위젯",
        "📅 날짜/시간 & 기타",
    ])

    with tab_text:
        show_text_inputs()

    with tab_number:
        show_numbers_sliders()

    with tab_selection:
        show_selections()

    with tab_datetime:
        show_date_time_extras()

