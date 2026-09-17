import streamlit as st
from components.layouts.columns import show_columns
from components.layouts.containers import show_containers
from components.layouts.expanders_popovers import show_expanders_popovers
from components.layouts.sidebars_empty import show_sidebars_empty

def show_layouts_tab():
    st.info("📐 **레이아웃 & 컨테이너 카테고리**: 아래 하위 탭을 통해 화면 배치 및 컨테이너 컴포넌트를 확인해보세요.")

    tab_col, tab_container, tab_expander, tab_sidebar = st.tabs([
        "🏛️ 컬럼 (Columns)",
        "📦 컨테이너 & 여백 (Container & Space)",
        "📑 아코디언 & 팝업 (Expander & Popover)",
        "📌 사이드바 & 플레이스홀더 (Sidebar & Empty)",
    ])

    with tab_col:
        show_columns()

    with tab_container:
        show_containers()

    with tab_expander:
        show_expanders_popovers()

    with tab_sidebar:
        show_sidebars_empty()

