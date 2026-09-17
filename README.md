# Streamlit Basic Showcase & AI Chatbot

Streamlit의 다양한 UI 컴포넌트 기능 탐색과 OpenAI API를 연동한 멀티모달 AI 챗봇 프로젝트입니다.

---

## 🚀 주요 기능

### 1. Streamlit 공식 Page Elements 종합 쇼케이스 (`app.py`)
공식 문서의 Page Elements 카테고리를 2단계 계층형 탭 구조로 구성하여 다양한 위젯과 옵션을 직접 체험할 수 있습니다:
- **✍️ Write and magic**: `st.write`, `st.write_stream`, Magic 문법
- **📝 Text elements**: Title, Markdown, Code, LaTeX, Divider 등
- **📊 Data elements**: `st.dataframe`, `st.data_editor`, `st.table`, `st.metric`, `st.json`
- **📈 Chart elements**: Line, Bar, Area, Scatter, Map 시각화
- **🎛️ Input widgets**: Text, Number, Slider, Select, Date/Time, Color 등
- **🎬 Media elements**: Image, Audio, Video
- **📐 Layouts and containers**: Columns, Container, Expander, Popover, Sidebar 등
- **💬 Chat elements**: Chat Message, Chat Input
- **🔔 Status elements**: Alerts, Progress, Spinner, Status, Toast, Balloons 등

### 2. OpenAI 멀티모달 챗봇 & 대화 히스토리 시스템 (`app2.py`)
Streamlit의 공식 멀티페이지 네비게이션(`st.navigation`)을 기반으로 구성되었습니다:
- **💬 AI 챗봇 대화 (`app2_chat.py`)**:
  - 기본 모델: `gpt-5.6-luna` (GPT 5.5+ 모델 선택 지원)
  - 🖼️ 이미지 업로드: 모달 팝업창(`@st.dialog`)에서 드래그 앤 드롭으로 이미지 첨부 및 Vision 분석
  - 📁 파일 업로드: 코드 및 문서 파일 첨부 시 컨텍스트 자동 주입
  - 실시간 타이핑 스트리밍 응답 (`st.write_stream`)
  - 대화 세션 분리 및 SQLite 영구 저장
- **📜 과거 대화 내역 뷰어 (`app2_history.py`)**:
  - SQLite(`chat_history.db`)에 저장된 모든 대화 세션 목록 조회 및 실시간 검색
  - 대화형 메시지 뷰(`st.chat_message`) 및 데이터 테이블 뷰(`st.dataframe`)
  - 대화 내역 텍스트(.txt) 및 CSV(.csv) 다운로드 지원

---

## 🛠️ 설치 및 실행 방법

### 1. 패키지 설치
이 프로젝트는 **uv**를 기본 패키지 매니저로 사용합니다:

```powershell
uv sync
```

### 2. 환경변수 설정
프로젝트 루트의 `.env` 파일에 OpenAI API Key를 설정합니다:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. 앱 실행

- **Page Elements 종합 쇼케이스 실행**:
  ```powershell
  uv run streamlit run app.py
  ```

- **OpenAI 챗봇 시스템 실행**:
  ```powershell
  uv run streamlit run app2.py
  ```
  *(또는 `run.bat` 실행)*
