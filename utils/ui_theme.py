import streamlit as st

def apply_custom_theme():
    """
    모든 페이지에 일관된 현대적이고 세련된 디자인 스타일(CSS)을 적용합니다.
    카드, 상태 뱃지, 버튼, 입력 위젯의 시각적 완성도를 높입니다.
    """
    st.markdown(
        """
        <style>
        /* 기본 폰트 및 부드러운 렌더링 */
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        
        * {
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', sans-serif;
        }

        /* 메인 컨테이너 패딩 최적화 */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 3rem !important;
            max-width: 1200px;
        }

        /* 세련된 카드 스타일 */
        .glass-card {
            background: rgba(128, 128, 128, 0.05);
            border: 1px solid rgba(128, 128, 128, 0.15);
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .glass-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
            border-color: rgba(99, 102, 241, 0.4);
        }

        /* 상태 뱃지 / 칩 스타일 */
        .status-chip {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 600;
        }
        .status-active {
            background-color: rgba(16, 185, 129, 0.12);
            color: #10b981;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        .status-inactive {
            background-color: rgba(245, 158, 11, 0.12);
            color: #f59e0b;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }
        .status-info {
            background-color: rgba(99, 102, 241, 0.12);
            color: #6366f1;
            border: 1px solid rgba(99, 102, 241, 0.3);
        }

        /* 메트릭 카드 시각 효과 */
        div[data-testid="stMetric"] {
            background: rgba(128, 128, 128, 0.05);
            border: 1px solid rgba(128, 128, 128, 0.12);
            border-radius: 12px;
            padding: 12px 16px;
        }

        /* 버튼 둥근 모서리 및 호버 스타일 */
        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        /* 사이드바 스타일링 */
        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(128, 128, 128, 0.15);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
