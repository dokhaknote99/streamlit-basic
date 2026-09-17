import streamlit as st

# 공식 문서 PAGE ELEMENTS 순서별 컴포넌트 임포트
from components.write_magic import show_write_magic_tab
from components.texts import show_texts_tab
from components.data import show_data_tab
from components.charts import show_charts_tab
from components.inputs import show_inputs_tab
from components.media import show_media_tab
from components.layouts import show_layouts_tab
from components.chat import show_chat_tab
from components.status import show_status_tab

st.set_page_config(
    page_title="Streamlit 공식 문서 Page Elements 종합 쇼케이스",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 Streamlit 공식 API: Page Elements 종합 쇼케이스")
st.caption("공식 문서의 Page Elements 카테고리별로 구성된 탭을 클릭하여 Streamlit의 모든 시각적 요소와 옵션들을 체험해보세요.")

# 최상위 9개 대분류 탭 (공식 문서 메뉴 순서 그대로 매핑)
(
    tab_write,
    tab_text,
    tab_data,
    tab_charts,
    tab_inputs,
    tab_media,
    tab_layouts,
    tab_chat,
    tab_status,
) = st.tabs([
    "✍️ Write and magic",
    "📝 Text elements",
    "📊 Data elements",
    "📈 Chart elements",
    "🎛️ Input widgets",
    "🎬 Media elements",
    "📐 Layouts and containers",
    "💬 Chat elements",
    "🔔 Status elements",
])

with tab_write:
    show_write_magic_tab()

with tab_text:
    show_texts_tab()

with tab_data:
    show_data_tab()

with tab_charts:
    show_charts_tab()

with tab_inputs:
    show_inputs_tab()

with tab_media:
    show_media_tab()

with tab_layouts:
    show_layouts_tab()

with tab_chat:
    show_chat_tab()

with tab_status:
    show_status_tab()
