import streamlit as st
from components.status.alerts import show_alerts
from components.status.progress_status import show_progress_status
from components.status.effects_toasts import show_effects_toasts

def show_status_tab():
    st.info("🔔 **Status Elements**: 알림 메시지, 로딩/진행 바, 축하 이펙트 등을 확인해보세요.")

    tab_alerts, tab_progress, tab_effects = st.tabs([
        "📢 알림 메시지 (Alerts)",
        "⏳ 진행률 & 상태 (Progress & Status)",
        "🎉 토스트 & 이펙트 (Toast & Effects)",
    ])

    with tab_alerts:
        show_alerts()

    with tab_progress:
        show_progress_status()

    with tab_effects:
        show_effects_toasts()

