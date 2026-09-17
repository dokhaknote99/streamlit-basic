# Streamlit Basic Showcase & AI Chatbot

Streamlit의 다양한 UI 컴포넌트 기능 탐색과 OpenAI API를 연동한 보안 중심 AI 챗봇 시스템 프로젝트입니다.

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

### 2. OpenAI AI 챗봇 시스템 (`app2.py`)
Streamlit의 공식 멀티페이지 네비게이션(`st.navigation`)을 기반으로 구성된 보안 강화 챗봇 시스템입니다:
- **👤 사용자 로그인 (`pages_app2/auth.py`)**:
  - 사용자 ID 기반 로그인으로 유저별 대화 세션 및 히스토리 완전 격리
  - 로그아웃 시 메모리 내 API Key 및 세션 데이터 즉시 영구 파기
- **🔑 API Key 등록 및 보안 안내 (`pages_app2/key_settings.py`)**:
  - **DB 절대 미저장 원칙**: 세션 메모리(`st.session_state`)에만 일시 보관
  - 보안 취약점 및 공용 PC 사용 주의사항 상세 안내
  - 등록된 Key 메모리에서 즉시 삭제 기능
- **💬 순수 텍스트 챗봇 (`pages_app2/chat.py`)**:
  - 불필요한 이미지/파일 업로드를 배제하고 텍스트 대화에만 집중
  - 기본 모델: `gpt-5.6-luna` (GPT 5.5+ 모델 선택 지원)
  - 실시간 타이핑 스트리밍 답변 (`st.write_stream`)
  - **세션당 100회 대화(200개 메시지) FIFO 자동 관리**: 초과 시 오래된 메시지 자동 삭제
  - **유저당 최대 10개 세션 FIFO 자동 관리**: 10개 초과 시 오래된 세션 자동 삭제
- **📜 과거 대화 내역 뷰어 (`pages_app2/history.py`)**:
  - 로그인한 사용자의 대화 기록(최대 10개 세션) 조회 및 실시간 검색
  - 대화형 메시지 뷰(`st.chat_message`) 및 데이터 테이블 뷰(`st.dataframe`)
  - 대화 내역 텍스트(.txt) 및 CSV(.csv) 다운로드 지원

---

## 🛠️ 설치 및 실행 방법

### 1. 패키지 설치
이 프로젝트는 **uv**를 기본 패키지 매니저로 사용합니다:

```powershell
uv sync
```

### 2. 앱 실행

- **Page Elements 종합 쇼케이스 실행**:
  ```powershell
  uv run streamlit run app.py
  ```

- **OpenAI 챗봇 시스템 실행**:
  ```powershell
  uv run streamlit run app2.py
  ```
  *(또는 `run.bat` 실행)*
