import base64
import os
import streamlit as st

@st.cache_data
def get_background_base64():
    """
    assets/background.jpg 이미지를 읽어 base64로 인코딩합니다.
    """
    image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "background.jpg")
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

def apply_custom_theme():
    """
    배경 이미지를 가림 없이 그대로 노출하고,
    불필요한 장식을 배제한 깔끔한 UI 스타일을 적용합니다.
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
            background-color: rgba(15, 23, 42, 0.75) !important;
            backdrop-filter: blur(12px) !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        }}
        [data-testid="stSidebar"] {{
            background-color: rgba(15, 23, 42, 0.75) !important;
            backdrop-filter: blur(12px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
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
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
            max-width: 1000px;
        }}

        /* 컨테이너 및 카드 글래스 반투명 (배경 투과) */
        div[data-testid="stVerticalBlockBorderWrapper"],
        .stChatMessage {{
            background: rgba(15, 23, 42, 0.6) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 12px !important;
        }}

        .stButton > button {{
            border-radius: 8px;
            font-weight: 600;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
