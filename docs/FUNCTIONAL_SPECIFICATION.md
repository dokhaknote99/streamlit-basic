# 📑 Streamlit Basic 프로젝트 기능 명세서 (Functional Specification)

본 문서는 `streamlit-basic` 프로젝트에 구현된 두 가지 주요 시스템(**Streamlit Page Elements 쇼케이스** 및 **OpenAI AI 챗봇 시스템**)의 각 페이지별 상세 기능과 동작 규격을 기술한 기능 명세서입니다.

---

## 🏛️ 1. 시스템 아키텍처 개요

```mermaid
graph TD
    subgraph App1 ["1. Page Elements 쇼케이스 (app.py)"]
        direction TB
        Tabs["9대 카테고리 계층형 탭"]
        Tabs --> T1["✍️ Write & Magic"]
        Tabs --> T2["📝 Text Elements"]
        Tabs --> T3["📊 Data Elements"]
        Tabs --> T4["📈 Chart Elements"]
        Tabs --> T5["🎛️ Input Widgets"]
        Tabs --> T6["🎬 Media Elements"]
        Tabs --> T7["📐 Layouts & Containers"]
        Tabs --> T8["💬 Chat Elements"]
        Tabs --> T9["🔔 Status Elements"]
    end

    subgraph App2 ["2. OpenAI AI 챗봇 시스템 (app2.py)"]
        direction TB
        Router["st.navigation 라우터"]
        Router --> Login["👤 로그인 (auth.py)"]
        Router --> KeyPage["🔑 Key 등록 (key_settings.py)"]
        Router --> ChatPage["💬 AI 챗봇 (chat.py)"]
        Router --> HistoryPage["📜 대화 내역 (history.py)"]
        
        KeyPage -.->|"휘발성 메모리 보관"| SessionState["st.session_state"]
        ChatPage <-->|"대화 기록/조회"| DB[("SQLite DB (chat_history.db)")]
        HistoryPage <-->|"세션/메시지 열람"| DB
    end
```

---

## 📱 2. 시스템 1: Streamlit Page Elements 쇼케이스 (`app.py`)

Streamlit 공식 문서의 `PAGE ELEMENTS` 9대 카테고리를 학습 및 탐색할 수 있도록 2단계 계층형 탭(최상위 탭 ➜ 서브 탭)으로 구성된 페이지입니다.

### 2.1. ✍️ Write and magic (`components/write_magic/`)
| 서브 탭 | 대상 API | 주요 기능 명세 |
| :--- | :--- | :--- |
| **st.write 기본 및 다양한 타입** | `st.write` | • 문자열, 마크다운, 다중 인자 출력<br>• 파이썬 딕셔너리 및 계층 구조 자동 서식화<br>• pandas DataFrame 전달 시 인터랙티브 테이블 자동 변환 |
| **스트리밍 & Magic 기능** | `st.write_stream`<br>Streamlit Magic | • 제너레이터를 통한 실시간 텍스트 타이핑 효과 렌더링<br>• `st.write()` 호출 없이 변수나 문자열 자체만으로 화면에 출력되는 Magic 문법 시연 |

### 2.2. 📝 Text elements (`components/texts/`)
| 서브 탭 | 대상 API | 주요 기능 명세 |
| :--- | :--- | :--- |
| **제목 및 캡션** | `st.title`, `st.header`<br>`st.subheader`, `st.text`<br>`st.caption`, `st.divider` | • 페이지 대/중/소 제목 계층 구조 표현<br>• 서식 없는 고정폭 일반 텍스트(`st.text`) 및 설명용 캡션(`st.caption`)<br>• 섹션 구분을 위한 가로선(`st.divider`) |
| **마크다운 & 컬러 서식** | `st.markdown` | • 굵게, 기울임, 취소선, 링크 등 기본 마크다운 문법<br>• Streamlit 고유 텍스트 컬러 태그(`:red[...]`, `:blue-background[...]`)<br>• 이모지 단축어(`:rocket:`, `:star:` 등) 렌더링 |
| **코드 및 LaTeX 수식** | `st.code`<br>`st.latex` | • 언어 지정(Python 등) 및 줄 번호(`line_numbers=True`)를 지원하는 구문 강조 코드 블록<br>• KaTeX 기반의 정밀한 수학 수식 렌더링 |

### 2.3. 📊 Data elements (`components/data/`)
| 서브 탭 | 대상 API | 주요 기능 명세 |
| :--- | :--- | :--- |
| **데이터프레임 & 에디터** | `st.dataframe`<br>`st.data_editor` | • 컬럼 정렬, 검색, 너비 맞춤(`width="stretch"`), 인덱스 숨김 지원 인터랙티브 테이블<br>• 브라우저에서 직접 셀 값을 더블클릭하여 수정하고 행을 동적으로 추가/삭제(`num_rows="dynamic"`)하는 스프레드시트 에디터 |
| **KPI 지표 & 테이블** | `st.metric`<br>`st.table` | • 주요 실적 지표(Value)와 전기 대비 증감(Delta) 및 색상 반전(`delta_color`) 표시<br>• 스크롤 없이 모든 셀이 고정 노출되는 정적 요약 테이블 |
| **JSON 트리 뷰** | `st.json` | • 계층형 JSON/딕셔너리 데이터를 접기/펼치기가 가능한 트리 뷰 형태로 시각화 |

### 2.4. 📈 Chart elements (`components/charts/`)
| 서브 탭 | 대상 API | 주요 기능 명세 |
| :--- | :--- | :--- |
| **선형 / 막대 / 영역 차트** | `st.line_chart`<br>`st.bar_chart`<br>`st.area_chart` | • DataFrame을 전달받아 설정 없이 자동 생성되는 꺾은선형 시계열 차트<br>• 카테고리별 비교 막대 차트<br>• 다중 지점 누적 추이를 보여주는 영역 차트 |
| **산점도 & 지도 (Map)** | `st.scatter_chart`<br>`st.map` | • 변수 간 상관관계 및 버블 크기(`size`)를 표현하는 산점도<br>• 위도(`latitude`)와 경도(`longitude`) 좌표 데이터를 지도 위에 핀 포인트로 시각화 |

### 2.5. 🎛️ Input widgets (`components/inputs/`)
| 서브 탭 | 대상 API | 주요 기능 명세 |
| :--- | :--- | :--- |
| **텍스트 입력** | `st.text_input`<br>`st.text_area` | • 기본값(`value`), 힌트 문구(`placeholder`), 도움말 툴팁(`help`)<br>• 비밀번호 마스킹(`type="password"`), 최대 글자 수 제한(`max_chars`)<br>• 라벨 숨김 모드(`label_visibility="visible"\|"hidden"\|"collapsed"`)<br>• 장문 입력용 높이 조절 텍스트 에어리어 |
| **숫자 & 슬라이더** | `st.number_input`<br>`st.slider`<br>`st.select_slider` | • 정수/실수 입력 및 증감 스텝(`step`), 포맷팅(`format="%.2f"`)<br>• 정수/실수 단일 슬라이더 및 구간 선택용 튜플 범위 슬라이더(`Range Slider`)<br>• 문자열 단계(만족도, 사이즈 등) 순차 선택 슬라이더 |
| **선택 위젯** | `st.radio`<br>`st.selectbox`<br>`st.multiselect`<br>`st.checkbox`<br>`st.toggle` | • 세로/가로형(`horizontal=True`) 및 캡션(`captions`) 지원 라디오 버튼<br>• 기본 선택 또는 빈 상태(`index=None`) 드롭다운<br>• 최대 개수 제한(`max_selections`) 지원 다중 태그 선택<br>• Boolean 체크박스 및 모던 스위치 토글 버튼 |
| **날짜/시간 & 기타** | `st.date_input`<br>`st.time_input`<br>`st.color_picker` | • 단일 예약일 및 기간 선택용 달력 튜플 범위 피커<br>• 단위 간격(`step=15분`) 지원 시간 피커<br>• HEX 색상 코드 및 팔레트 색상 선택기 |

### 2.6. 🎬 Media elements (`components/media/`)
| 서브 탭 | 대상 API | 주요 기능 명세 |
| :--- | :--- | :--- |
| **이미지 & 로고** | `st.image` | • 웹 URL 및 로컬 파일 이미지를 캡션 및 너비 맞춤(`width="stretch"`)으로 렌더링 |
| **오디오 & 비디오** | `st.audio`<br>`st.video` | • 사운드 파일 스트림/URL 재생 오디오 플레이어<br>• 유튜브 영상 및 mp4 동영상 임베드 비디오 플레이어 |

### 2.7. 📐 Layouts and containers (`components/layouts/`)
| 서브 탭 | 대상 API | 주요 기능 명세 |
| :--- | :--- | :--- |
| **컬럼 (Columns)** | `st.columns` | • 가로 균등 분할 및 가중 비율(`[3, 1]`) 분할<br>• 수직 정렬(`vertical_alignment="center"`) 및 간격(`gap="medium"`) 제어 |
| **컨테이너 & 여백** | `st.container`<br>`st.space`<br>`st.bottom` | • 카드 스타일 테두리(`border=True`) 그룹화<br>• 고정 높이 스크롤 박스(`height=130`)<br>• 요소 간 유연한 공간 추가(`size="large"`)<br>• 브라우저 최하단에 항상 고정되는 Footer 바닥글 컨테이너 |
| **아코디언 & 팝업** | `st.expander`<br>`st.popover`<br>`st.tabs` | • 접기/펼치기 및 초기 펼침(`expanded=True`), 아이콘 설정 아코디언<br>• 버튼 클릭 시 오버레이로 열리는 팝업 메뉴 컨테이너<br>• 컴포넌트 레벨의 중첩 탭 네비게이션 |
| **사이드바 & 플레이스홀더** | `st.sidebar`<br>`st.empty` | • 화면 좌측 패널에 위젯을 상시 배치하는 사이드바 제어<br>• 특정 위치의 콘텐츠를 동적으로 갱신하거나 비우는 단일 요소 플레이스홀더 |

### 2.8. 💬 Chat elements (`components/chat/`)
| 서브 탭 | 대상 API | 주요 기능 명세 |
| :--- | :--- | :--- |
| **챗 메시지 & 입력** | `st.chat_message`<br>`st.chat_input` | • 사용자(`user`) 및 어시스턴트(`assistant`) 대화 버블<br>• 커스텀 아바타(이모지 등) 적용<br>• 화면 하단 고정형 대화 입력창 |

### 2.9. 🔔 Status elements (`components/status/`)
| 서브 탭 | 대상 API | 주요 기능 명세 |
| :--- | :--- | :--- |
| **알림 메시지 (Alerts)** | `st.success`, `st.info`<br>`st.warning`, `st.error`<br>`st.exception` | • 성공(초록), 안내(파랑), 경고(노랑), 오류(빨강) 상태 알림 배너<br>• 예외 객체 및 스택트레이스 시각화 |
| **진행률 & 상태** | `st.spinner`<br>`st.progress`<br>`st.status` | • 비동기 작업 대기용 회전 로딩 스피너<br>• 퍼센트 단위(0~100%) 프로그레스 바<br>• 다단계 복합 작업의 실시간 진행 현황을 접기/펼치기로 안내하는 상태 컨테이너 |
| **토스트 & 이펙트** | `st.toast`<br>`st.balloons`<br>`st.snow` | • 우측 하단에 일시적으로 떴다 사라지는 토스트 팝업<br>• 축하 풍선 날리기 및 겨울 눈송이 내리기 시각 효과 |

---

## 🤖 3. 시스템 2: OpenAI AI 챗봇 시스템 (`app2.py`)

Streamlit 공식 멀티페이지 네비게이션(`st.navigation`)과 SQLite를 기반으로 유저 격리, 세션 메모리 보안, 대화 수명 주기(FIFO) 관리를 지원하는 프로덕션 레벨 챗봇 시스템입니다.

### 3.1. 라우터 및 상태 제어 (`app2.py`)
- **로그인 분기 라우팅**:
  - `st.session_state["user_id"]` 미존재 시: 오직 **`👤 로그인`** 페이지만 사이드바에 노출.
  - 로그인 성공 시: **`💬 챗봇 서비스`**, **`📜 데이터 관리`**, **`👤 계정`** 그룹 메뉴 활성화.
- **사이드바 글로벌 컨트롤**:
  - 접속자 ID 및 API Key 등록 상태 표시 (`✅ 등록됨` / `⚠️ 미등록`)
  - **`[🚪 로그아웃]` 버튼**: 메모리에 존재하는 `user_id`, `openai_api_key`, `current_session_id`를 즉시 영구 파기하고 초기 화면으로 이동.

---

### 3.2. 👤 로그인 페이지 (`pages_app2/auth.py`)
| 기능 항목 | 상세 명세 |
| :--- | :--- |
| **사용자 식별 (Login)** | • 사용자 ID(텍스트)를 입력받아 세션 상태(`st.session_state["user_id"]`)에 바인딩<br>• 복잡한 가입 절차 없이 닉네임만으로 즉시 본인만의 격리된 작업 환경 생성 |
| **상태 피드백** | • 로그인 완료 시 현재 접속자명 표시 및 안내 문구 노출 |
| **로그아웃** | • 계정 정보 화면 내에서도 로그아웃 기능 직접 지원 |

---

### 3.3. 🔑 API Key 등록 및 보안 안내 (`pages_app2/key_settings.py`)
| 기능 항목 | 상세 명세 |
| :--- | :--- |
| **보안 취약점 경고 배너** | • **DB 미저장 원칙**: 입력된 키는 DB나 파일에 절대 쓰이지 않음을 명시<br>• **세션 휘발성 안내**: 브라우저 탭 세션 메모리에만 일시 보관되며 창 닫기/로그아웃 시 소멸됨을 안내<br>• **공용 PC 주의사항**: 사용 후 키 삭제 또는 로그아웃 필수 권고<br>• **키 유출 방지**: 타인 노출 금지 지침 전달 |
| **Key 등록 폼** | • `password` 타입 입력 필드로 키 마스킹 처리<br>• `st.session_state["openai_api_key"]`에만 저장 (환경변수 의존성 배제) |
| **Key 상태 표시 & 즉시 삭제** | • 등록 완료 시 마스킹된 형태(`sk-...XXXX`)로 등록 상태 표시<br>• `[등록된 API Key 삭제]` 버튼을 통해 세션 메모리에서 언제든지 즉각 파기 가능 |

---

### 3.4. 💬 순수 텍스트 AI 챗봇 (`pages_app2/chat.py`)
| 기능 항목 | 상세 명세 |
| :--- | :--- |
| **API Key 사전 검증** | • 세션 메모리에 키가 없을 경우 안내 배너(`st.warning`)를 띄우고 입력창 차단 (`st.stop`) |
| **순수 텍스트 대화** | • 이미지/파일 업로드 코드를 전면 배제하고 순수 텍스트 대화에만 집중<br>• `st.chat_input` 및 `st.chat_message` 활용 |
| **최신 LLM 모델 적용** | • 기본 모델: 규칙에 따라 **`gpt-5.6-luna`** 기본 설정<br>• 사이드바를 통해 GPT 5.5+ 라인업(`gpt-5.6-luna`, `gpt-5.6-terra`, `gpt-5.6-sol`, `gpt-5.5`, `gpt-6-astra`) 선택 가능 |
| **실시간 스트리밍 답변** | • `st.write_stream`과 OpenAI Stream Generator를 연동하여 글자가 실시간 타이핑되는 효과 제공 |
| **스마트 제목 갱신** | • 새 대화 세션의 첫 질문이 전송되면 질문 앞부분(최대 30자)으로 세션 제목을 자동 갱신 |
| **대화 수명 주기 (FIFO)** | • **세션당 최대 100회(200개 메시지)** 저장: 초과 시 가장 오래된 메시지 쌍부터 자동 삭제 |
| **세션 수명 주기 (FIFO)** | • **유저당 최대 10개 세션** 유지: `[➕ 새 대화 시작]` 시 10개를 초과하면 가장 오래된 세션 자동 삭제 |
| **사이드바 세션 전환** | • 드롭다운을 통해 본인의 과거 세션(최대 10개)을 즉시 전환하여 대화 지속 가능 |

---

### 3.5. 📜 과거 대화 내역 뷰어 (`pages_app2/history.py`)
| 기능 항목 | 상세 명세 |
| :--- | :--- |
| **유저별 세션 필터링** | • 로그인한 `user_id`의 세션(최대 10개)만 조회하여 타 사용자의 데이터 완전 차단 |
| **실시간 세션 검색** | • 세션 제목 키워드 검색 필터 제공 |
| **세션 메트릭 카드** | • 선택된 대화의 제목, 생성 일시, 총 메시지 수를 상단 지표 카드로 요약 |
| **💬 대화형 메시지 뷰** | • 실제 챗봇 UI와 동일한 대화 버블로 발송 시각과 메시지 원본 렌더링<br>• **`[텍스트 다운로드 (.txt)]`**: 대화 전체 내용을 텍스트 파일로 내보내기 |
| **📊 데이터 테이블 뷰** | • 원본 데이터베이스 레코드를 표 형식으로 확인<br>• **`[CSV 다운로드 (.csv)]`**: UTF-8 BOM 인코딩 엑셀 호환 CSV 파일 다운로드 |
| **세션 개별 삭제** | • 특정 세션과 소속 메시지들을 DB에서 즉시 영구 삭제 |

---

## 🗄️ 4. 데이터베이스 및 보안 아키텍처 명세 (`utils/db.py`)

### 4.1. 스키마 정의 (`chat_history.db`)
```sql
-- 대화 세션 테이블 (Key 정보 일절 없음)
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,               -- 세션 고유 ID (session_YYYYMMDD_HHMMSS_ffffff)
    user_id TEXT,                      -- 소유 사용자 ID (로그인 계정)
    title TEXT,                        -- 대화방 제목 (첫 질문 자동 반영)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 메시지 테이블 (Key 정보 일절 없음)
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,                   -- 소속 세션 ID (외래키 역할)
    role TEXT,                         -- 발신 주체 ('user' 또는 'assistant')
    content TEXT,                      -- 메시지 텍스트 본문
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4.2. FIFO 보관 정책 알고리즘
```mermaid
flowchart TD
    subgraph MsgFIFO ["1. 세션당 메시지 FIFO (최대 100회 = 200개)"]
        NewMsg["save_message(session_id, role, content)"] --> InsertM["INSERT INTO messages"]
        InsertM --> CountM{"해당 세션 메시지 수 > 200개?"}
        CountM -- "Yes" --> DelOldM["가장 오래된 초과분 메시지 DELETE"]
        CountM -- "No" --> EndM["완료"]
        DelOldM --> EndM
    end

    subgraph SessFIFO ["2. 유저당 세션 FIFO (최대 10개)"]
        NewSess["create_session(user_id, title)"] --> InsertS["INSERT INTO sessions"]
        InsertS --> CountS{"해당 유저 세션 수 > 10개?"}
        CountS -- "Yes" --> DelOldS["가장 오래된 세션의 messages 및 sessions DELETE"]
        CountS -- "No" --> EndS["완료"]
        DelOldS --> EndS
    end
```

### 4.3. 보안 규칙 검증 명세
1. **API Key 미저장**: `chat_history.db`의 모든 테이블과 쿼리에는 API Key 필드가 없으며, 파일 디스크나 로그에 키를 남기지 않습니다.
2. **세션 메모리 생명주기**: API Key는 오직 `st.session_state["openai_api_key"]`에만 존재하며, 브라우저 탭 닫기, 새로고침, 로그아웃 시 가비지 컬렉터에 의해 즉시 소멸됩니다.
