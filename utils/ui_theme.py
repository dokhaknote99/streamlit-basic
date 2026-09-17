import base64
import html
import os
import streamlit as st

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")


@st.cache_data
def get_asset_base64(filename: str) -> str:
    """
    assets/ 폴더의 이미지를 base64 문자열로 인코딩합니다. (없으면 빈 문자열)
    """
    image_path = os.path.join(ASSETS_DIR, filename)
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


def get_background_base64() -> str:
    """assets/background.jpg(밝은 계열 배경 이미지)를 base64로 인코딩합니다."""
    return get_asset_base64("background.jpg")


def apply_custom_theme():
    """
    밝고 화사한 라이트 글래스모피즘 테마를 적용합니다.
    - 배경 이미지 위에 흰색 베일을 얹어 콘텐츠 가독성 확보
    - 상단 네비게이션을 알약(pill) 형태로, 카드/버튼/입력창을 둥글고 부드럽게
    - 채팅 말풍선을 사용자(우측, 인디고) / AI(좌측, 화이트)로 구분
    """
    bg_base64 = get_background_base64()
    bg_layer = (
        f', url("data:image/jpeg;base64,{bg_base64}")' if bg_base64 else ""
    )

    st.markdown(
        f"""
        <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

        :root {{
            --brand: #4f46e5;
            --brand-2: #6366f1;
            --brand-soft: rgba(79, 70, 229, 0.10);
            --ink: #0f172a;
            --muted: #64748b;
            --line: rgba(15, 23, 42, 0.08);
            --card: rgba(255, 255, 255, 0.86);
            --shadow-card: 0 12px 32px -14px rgba(30, 41, 99, 0.22);
            --shadow-soft: 0 2px 10px rgba(30, 41, 99, 0.05);
        }}

        /* ── 배경: 이미지 위에 밝은 베일 ─────────────────────────── */
        .stApp {{ background: transparent !important; }}
        [data-testid="stAppViewContainer"] {{
            background-image:
                linear-gradient(180deg, rgba(255,255,255,0.62) 0%, rgba(255,255,255,0.40) 45%, rgba(255,255,255,0.55) 100%){bg_layer};
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }}

        /* ── 상단 헤더 & 네비게이션 ─────────────────────────────── */
        [data-testid="stHeader"] {{
            background: rgba(255, 255, 255, 0.72) !important;
            backdrop-filter: blur(18px) saturate(160%) !important;
            -webkit-backdrop-filter: blur(18px) saturate(160%) !important;
            border-bottom: 1px solid var(--line) !important;
        }}
        [data-testid="stTopNavLink"] {{
            border-radius: 999px !important;
            padding: 0 14px !important;
            height: 34px !important;
            font-weight: 600 !important;
            color: var(--muted) !important;
            background: transparent !important;
            transition: background .15s ease, color .15s ease !important;
        }}
        [data-testid="stTopNavLink"]:hover {{
            background: rgba(15, 23, 42, 0.05) !important;
            color: var(--ink) !important;
        }}
        [data-testid="stTopNavLink"][aria-current="page"] {{
            background: var(--brand-soft) !important;
            color: var(--brand) !important;
        }}
        [data-testid="stTopNavLink"][aria-current="page"] p {{ color: var(--brand) !important; }}
        [data-testid="stHeaderLogo"] {{
            height: 34px !important;
            border-radius: 10px !important;
        }}
        [data-testid="stAppDeployButton"] {{ display: none !important; }}

        /* ── 사이드바 ───────────────────────────────────────────── */
        [data-testid="stSidebar"] {{
            background: rgba(255, 255, 255, 0.92) !important;
            backdrop-filter: blur(18px) !important;
            -webkit-backdrop-filter: blur(18px) !important;
            border-right: 1px solid var(--line) !important;
        }}
        [data-testid="stSidebarHeader"] {{ padding: 14px 18px 4px !important; }}
        [data-testid="stSidebarLogo"] {{
            height: 40px !important;
            max-width: 170px !important;
            object-fit: contain !important;
        }}
        [data-testid="stSidebarUserContent"] {{ padding: 6px 18px 40px !important; }}
        [data-testid="stSidebar"] hr {{ margin: 12px 0 !important; }}

        /* 사이드바 대화 목록 (radio → 리스트 형태) */
        [class*="st-key-session_list"] [data-testid="stRadioOption"] {{
            display: flex !important;
            width: 100% !important;
            padding: 8px 12px !important;
            margin: 2px 0 !important;
            border-radius: 10px !important;
            transition: background .12s ease !important;
        }}
        [class*="st-key-session_list"] [data-testid="stRadioOption"]:hover {{
            background: rgba(15, 23, 42, 0.045) !important;
        }}
        [class*="st-key-session_list"] [data-testid="stRadioOption"][data-selected="true"] {{
            background: var(--brand-soft) !important;
        }}
        [class*="st-key-session_list"] [data-testid="stRadioOption"][data-selected="true"] p {{
            color: var(--brand) !important;
            font-weight: 600 !important;
        }}
        [class*="st-key-session_list"] [data-testid="stRadioOption"] > div > div:first-child {{
            display: none !important;   /* 라디오 동그라미 숨김 */
        }}
        [class*="st-key-session_list"] [data-testid="stRadioOption"] p {{
            font-size: 0.9rem !important;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        [class*="st-key-session_list"] [data-testid="stRadioOption"] [data-testid="stMarkdownContainer"] {{
            min-width: 0;
            overflow: hidden;
        }}

        /* ── 본문 레이아웃 ──────────────────────────────────────── */
        .block-container {{
            padding-top: 2.2rem !important;
            padding-bottom: 2rem !important;
            max-width: 1080px;
        }}

        /* ── 카드 (key="card_*" 컨테이너) ────────────────────────── */
        [class*="st-key-card"] > [data-testid="stVerticalBlock"],
        [class*="st-key-card"][data-testid="stVerticalBlock"] {{
            background: var(--card) !important;
            backdrop-filter: blur(14px) !important;
            -webkit-backdrop-filter: blur(14px) !important;
            border: 1px solid rgba(255, 255, 255, 0.9) !important;
            border-radius: 20px !important;
            box-shadow: var(--shadow-card), 0 0 0 1px var(--line) !important;
            padding: 1.35rem 1.5rem !important;
        }}

        /* ── 페이지 헤더 ────────────────────────────────────────── */
        .app-page-header {{
            display: flex; align-items: center; gap: 14px;
            margin: 0 0 18px;
        }}
        .app-page-icon {{
            flex: 0 0 auto;
            width: 48px; height: 48px; border-radius: 15px;
            display: flex; align-items: center; justify-content: center;
            font-size: 24px; line-height: 1;
            background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%);
            box-shadow: inset 0 0 0 1px rgba(79, 70, 229, 0.14), 0 6px 14px -8px rgba(79,70,229,.45);
        }}
        .app-page-title {{
            font-size: 1.55rem; font-weight: 700; letter-spacing: -0.02em;
            color: var(--ink); line-height: 1.2;
        }}
        .app-page-subtitle {{
            font-size: 0.9rem; color: var(--muted); margin-top: 4px;
            display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
        }}
        .app-chip {{
            display: inline-flex; align-items: center; gap: 5px;
            padding: 2px 10px; border-radius: 999px;
            background: var(--brand-soft); color: var(--brand);
            font-weight: 600; font-size: 0.78rem; letter-spacing: -0.01em;
        }}
        .app-chip.gray {{ background: rgba(15,23,42,.06); color: var(--muted); }}
        .app-chip.green {{ background: rgba(16,185,129,.12); color: #047857; }}
        .app-chip.amber {{ background: rgba(245,158,11,.14); color: #b45309; }}

        /* ── 빈 상태(empty state) ───────────────────────────────── */
        .app-empty {{
            min-height: 220px;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            text-align: center; gap: 6px; padding: 24px;
        }}
        .app-empty img {{
            width: 84px; height: 84px; border-radius: 24px; object-fit: cover;
            box-shadow: 0 10px 24px -10px rgba(79,70,229,.45);
            margin-bottom: 10px;
        }}
        .app-empty-title {{ font-size: 1.2rem; font-weight: 700; color: var(--ink); letter-spacing: -0.01em; }}
        .app-empty-sub {{ font-size: 0.92rem; color: var(--muted); max-width: 380px; line-height: 1.55; }}
        [class*="st-key-card_chat"] .app-empty {{ min-height: 440px; }}

        /* ── 채팅 말풍선 ────────────────────────────────────────── */
        .stChatMessage {{
            background: transparent !important;
            padding: 6px 0 !important;
            gap: 10px !important;
            align-items: flex-start !important;
        }}
        .stChatMessage [data-testid="stChatMessageContent"] {{
            background: #ffffff;
            border: 1px solid var(--line);
            border-radius: 18px 18px 18px 6px;
            padding: 12px 16px;
            box-shadow: var(--shadow-soft);
            max-width: 82%;
            flex: 0 1 auto !important;
        }}
        .stChatMessage:has([data-testid="stChatMessageAvatarUser"]) {{
            flex-direction: row-reverse !important;
        }}
        .stChatMessage:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {{
            background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
            border: none;
            border-radius: 18px 18px 6px 18px;
            box-shadow: 0 8px 20px -10px rgba(79,70,229,.6);
        }}
        .stChatMessage:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] :is(p, li, span, code, h1, h2, h3, h4) {{
            color: #ffffff !important;
        }}
        .stChatMessage:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] code {{
            background: rgba(255,255,255,.18) !important;
        }}
        [data-testid="stChatMessageAvatarUser"] {{
            background: var(--brand) !important;
            border-radius: 12px !important;
            color: #fff !important;
        }}
        [data-testid="stChatMessageAvatarAssistant"],
        .stChatMessage img[data-testid="stChatMessageAvatarCustom"] {{
            background: #ffffff !important;
            border-radius: 12px !important;
            box-shadow: 0 0 0 1px var(--line);
        }}
        .stChatMessage [data-testid="stCaptionContainer"] p {{ font-size: 0.75rem !important; }}

        /* ── 채팅 입력창 ────────────────────────────────────────── */
        [data-testid="stBottom"] > div {{
            background: linear-gradient(180deg, rgba(255,255,255,0) 0%, rgba(255,255,255,.85) 40%) !important;
        }}
        [data-testid="stBottomBlockContainer"] {{
            max-width: 1080px !important;
            padding-top: 0.6rem !important;
            padding-bottom: 1.6rem !important;
        }}
        [data-testid="stChatInput"] > div:first-child {{
            background: #ffffff !important;
            border: 1px solid var(--line) !important;
            border-radius: 16px !important;
            box-shadow: 0 10px 28px -14px rgba(30, 41, 99, 0.35) !important;
            transition: border-color .15s ease, box-shadow .15s ease !important;
        }}
        [data-testid="stChatInput"] > div:first-child:focus-within {{
            border-color: var(--brand) !important;
            box-shadow: 0 0 0 4px var(--brand-soft), 0 10px 28px -14px rgba(30, 41, 99, 0.35) !important;
        }}
        [data-testid="stChatInputSubmitButton"] {{
            background: var(--brand) !important;
            color: #fff !important;
            border-radius: 10px !important;
            margin: 4px !important;
        }}
        [data-testid="stChatInputSubmitButton"]:hover {{ background: #4338ca !important; }}

        /* ── 버튼 ────────────────────────────────────────────────── */
        .stButton > button, .stDownloadButton > button, .stLinkButton > a, [data-testid="stFormSubmitButton"] > button {{
            font-weight: 600 !important;
            transition: transform .08s ease, box-shadow .15s ease, filter .15s ease !important;
        }}
        [data-testid="stBaseButton-primary"] {{
            background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
            border: none !important;
            box-shadow: 0 8px 18px -8px rgba(79, 70, 229, 0.65) !important;
        }}
        [data-testid="stBaseButton-primary"]:hover {{
            filter: brightness(1.06);
            transform: translateY(-1px);
        }}
        [data-testid="stBaseButton-secondary"] {{
            background: #ffffff !important;
            border: 1px solid rgba(15, 23, 42, 0.12) !important;
            box-shadow: var(--shadow-soft) !important;
        }}
        [data-testid="stBaseButton-secondary"]:hover {{
            border-color: var(--brand) !important;
            color: var(--brand) !important;
        }}

        /* ── 입력 위젯 ──────────────────────────────────────────── */
        [data-testid="stTextInput"] input,
        [data-testid="stTextInput"] > div > div,
        [data-testid="stSelectbox"] > div > div {{
            background: #ffffff !important;
        }}
        [data-testid="stTextInput"] > div > div,
        [data-testid="stSelectbox"] > div > div {{
            border-radius: 12px !important;
        }}
        [data-testid="stWidgetLabel"] p {{
            font-weight: 600 !important;
            color: var(--ink) !important;
        }}

        /* ── 이미지 / 알림 / 탭 / 메트릭 ─────────────────────────── */
        [data-testid="stImage"] img {{ border-radius: 16px; }}
        [data-testid="stAlert"] {{ border-radius: 14px !important; }}
        [data-testid="stMetric"] {{
            background: #f8fafc;
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 12px 16px !important;
        }}
        [data-testid="stMetricLabel"] p {{ color: var(--muted) !important; font-weight: 600 !important; }}
        [data-testid="stTab"] {{ font-weight: 600 !important; }}
        [data-testid="stExpander"] details {{
            border-radius: 14px !important;
            background: rgba(255,255,255,.7) !important;
        }}
        [data-testid="stDataFrame"] {{ border-radius: 14px; overflow: hidden; }}
        hr {{ border-color: var(--line) !important; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(icon: str, title: str, subtitle: str | None = None, chips: list[tuple[str, str]] | None = None):
    """
    아이콘 + 제목 + (부제/칩) 형태의 공통 페이지 헤더를 렌더링합니다.
    chips: [(라벨, 색상)] 형태. 색상은 "" | "gray" | "green" | "amber".
    """
    chip_html = "".join(
        f'<span class="app-chip {html.escape(color)}">{html.escape(label)}</span>'
        for label, color in (chips or [])
    )
    sub_parts = []
    if subtitle:
        sub_parts.append(f"<span>{html.escape(subtitle)}</span>")
    if chip_html:
        sub_parts.append(chip_html)
    sub_html = f'<div class="app-page-subtitle">{"".join(sub_parts)}</div>' if sub_parts else ""

    st.markdown(
        f"""
        <div class="app-page-header">
            <div class="app-page-icon">{icon}</div>
            <div style="min-width:0">
                <div class="app-page-title">{html.escape(title)}</div>
                {sub_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state(title: str, subtitle: str, image: str = "logo.jpg"):
    """로고 + 안내 문구가 가운데 정렬된 빈 상태(empty state) 블록을 렌더링합니다."""
    b64 = get_asset_base64(image)
    img_html = f'<img src="data:image/jpeg;base64,{b64}" alt="">' if b64 else ""
    st.markdown(
        f"""
        <div class="app-empty">
            {img_html}
            <div class="app-empty-title">{html.escape(title)}</div>
            <div class="app-empty-sub">{html.escape(subtitle)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def session_labels(sessions) -> dict:
    """
    세션 행 목록([(id, title, created_at, ...), ...])을 {id: 고유 라벨} 딕셔너리로 변환합니다.
    같은 제목이 여러 개면 " (2)", " (3)"을 붙여 구분합니다.
    (Streamlit 라디오는 라벨이 중복되면 선택 상태를 잘못 표시하므로 고유 라벨이 필요)
    """
    labels: dict = {}
    seen: dict = {}
    for row in sessions:
        sid, title = row[0], row[1]
        count = seen.get(title, 0) + 1
        seen[title] = count
        labels[sid] = title if count == 1 else f"{title} ({count})"
    return labels
