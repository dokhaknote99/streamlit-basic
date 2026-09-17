import base64
import os
import streamlit as st

@st.cache_data
def get_background_base64():
    """
    assets/background.jpg(밝은 계열 배경 이미지)를 읽어 base64로 인코딩합니다.
    """
    image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "background.jpg")
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

def apply_custom_theme():
    """
    밝고 화사한 라이트 글래스모피즘 테마 및 배경 이미지를 적용합니다.
    """
    bg_base64 = get_background_base64()
    bg_style = ""
    if bg_base64:
        bg_style = f"""
        .stApp {{
            background-color: transparent !important;
        }}
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/jpeg;base64,{bg_base64}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }}
        [data-testid="stHeader"] {{
            background-color: rgba(255, 255, 255, 0.82) !important;
            backdrop-filter: blur(14px) !important;
            border-bottom: 1px solid rgba(0, 0, 0, 0.06) !important;
        }}
        [data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.88) !important;
            backdrop-filter: blur(14px) !important;
            border-right: 1px solid rgba(0, 0, 0, 0.08) !important;
        }}
        """

    st.markdown(
        f"""
        <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        
        * {{
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
        }}

        {bg_style}

        .block-container {{
            padding-top: 1.8rem !important;
            padding-bottom: 2rem !important;
            max-width: 1060px;
        }}

        /* 컨테이너 및 폼 라이트 글래스 반투명 효과 */
        div[data-testid="stVerticalBlockBorderWrapper"],
        div[data-testid="stForm"] {{
            background: rgba(255, 255, 255, 0.82) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(0, 0, 0, 0.08) !important;
            border-radius: 14px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04) !important;
        }}

        /* 채팅 메시지 버블 라이트 모드 최적화 */
        .stChatMessage {{
            background: rgba(255, 255, 255, 0.9) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(0, 0, 0, 0.07) !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) !important;
            margin-bottom: 8px !important;
        }}

        .stButton > button {{
            border-radius: 8px;
            font-weight: 600;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
