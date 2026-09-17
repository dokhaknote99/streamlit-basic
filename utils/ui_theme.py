import base64
import os
import streamlit as st

@st.cache_data
def get_background_base64():
    """
    assets/background.jpg 이미지를 읽어 base64 문자열로 인코딩합니다.
    캐싱을 적용하여 페이지 리런 시 반복 디스크 I/O를 방지합니다.
    """
    image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "background.jpg")
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

def apply_custom_theme():
    """
    모든 페이지에 일관된 현대적이고 세련된 디자인 스타일(CSS)과 배경 이미지를 적용합니다.
    """
    bg_base64 = get_background_base64()
    bg_style = ""
    if bg_base64:
        bg_style = f"""
        /* 메인 앱 배경 이미지 및 부드러운 다크 오버레이 */
        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(rgba(15, 23, 42, 0.84), rgba(15, 23, 42, 0.92)), url("data:image/jpeg;base64,{bg_base64}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }}

        /* 상단 헤더 투명화 */
        [data-testid="stHeader"] {{
            background-color: transparent !important;
        }}

        /* 사이드바 글래스모피즘 블러 효과 */
        [data-testid="stSidebar"] {{
            background-color: rgba(15, 23, 42, 0.85) !important;
            backdrop-filter: blur(14px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        }}
        """

    st.markdown(
        f"""
        <style>
        /* 기본 폰트 및 부드러운 렌더링 */
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        
        * {{
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', sans-serif;
        }}

        {bg_style}

        /* 메인 컨테이너 패딩 최적화 */
        .block-container {{
            padding-top: 2rem !important;
            padding-bottom: 3rem !important;
            max-width: 1200px;
        }}

        /* 세련된 카드 스타일 */
        .glass-card {{
            background: rgba(30, 41, 59, 0.6) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }}
        .glass-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
            border-color: rgba(99, 102, 241, 0.5) !important;
        }}

        /* 상태 뱃지 / 칩 스타일 */
        .status-chip {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 600;
        }}
        .status-active {{
            background-color: rgba(16, 185, 129, 0.18);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.4);
        }}
        .status-inactive {{
            background-color: rgba(245, 158, 11, 0.18);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.4);
        }}
        .status-info {{
            background-color: rgba(99, 102, 241, 0.18);
            color: #818cf8;
            border: 1px solid rgba(99, 102, 241, 0.4);
        }}

        /* 메트릭 카드 시각 효과 */
        div[data-testid="stMetric"] {{
            background: rgba(30, 41, 59, 0.55) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px;
            padding: 12px 16px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}

        /* 기본 컨테이너 보더 블러 처리 */
        [data-testid="stVerticalBlockBorderWrapper"] {{
            background: rgba(30, 41, 59, 0.45);
            backdrop-filter: blur(8px);
            border-radius: 14px;
        }}

        /* 채팅 메시지 배경 */
        [data-testid="stChatMessage"] {{
            background: rgba(30, 41, 59, 0.5) !important;
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            margin-bottom: 8px;
        }}

        /* 버튼 둥근 모서리 및 호버 스타일 */
        .stButton > button {{
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.2s ease;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
