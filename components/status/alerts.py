import streamlit as st

def show_alerts():
    st.header("🔔 알림 메시지 박스 (Alerts)")
    st.caption("작업 결과나 사용자 주의를 환기시키는 상태 알림 배너입니다.")

    st.success("✅ 성공 (st.success): 파일 업로드가 정상적으로 완료되었습니다.", icon="✅")
    st.info("ℹ️ 안내 (st.info): 새로운 기능이 업데이트되었습니다.", icon="ℹ️")
    st.warning("⚠️ 경고 (st.warning): 비밀번호 유효기간이 3일 남았습니다.", icon="⚠️")
    st.error("🚨 오류 (st.error): 서버 연결에 실패했습니다. 다시 시도해주세요.", icon="🚨")

    st.write("예외 메시지 (st.exception):")
    # st.exception(RuntimeError("네트워크 타임아웃 예외가 발생했습니다."))

