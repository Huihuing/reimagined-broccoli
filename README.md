# Mini Watch — React + Flask 감시 대시보드

기존 `mini-watch`의 일반 게시판을 유지하면서, 운영자가 로그인해 요청 기록을 확인하고 관찰 메모를 관리하는 감시 대시보드를 완성한 프로젝트입니다.

이번 단계에서는 기존 `general/` 게시판과 요청 기록 전송 코드를 유지하고, `monitor/backend/`에 Flask JSON API와 PostgreSQL 저장 기능을 확장했으며 `monitor/frontend/`에 Vite + React 화면을 새로 구현했습니다.

## 사용 기술

- 일반 서비스: Python, Flask, Jinja2, PostgreSQL, psycopg, requests
- 감시 API: Python, Flask, PostgreSQL, psycopg
- 감시 화면: React, Vite, JavaScript, CSS
- 인증: PostgreSQL 운영자 계정 + Werkzeug 비밀번호 해시 + Flask session cookie
- 개발 포트
  - 일반 게시판: `5100`
  - 감시 Flask API: `5200`
  - React/Vite: `5173`

React는 DB에 직접 접속하지 않습니다. 모든 로그인, 요청 기록 조회, 메모 CRUD는 Vite의 `/api` 프록시를 거쳐 Flask API에서 처리합니다.

## 프로젝트 구조

```text
reimagined-broccoli/
├─ general/
│  ├─ app.py
│  ├─ db.py
│  ├─ post_rules.py
│  ├─ request_logging.py
│  ├─ requirements.txt
│  ├─ .env.example
│  ├─ repositories/
│  ├─ routes/
│  ├─ templates/
│  ├─ static/
│  ├─ sql/
│  │  └─ 001_create_posts.sql
│  └─ tests/
│
├─ monitor/
│  ├─ backend/
│  │  ├─ app.py
│  │  ├─ db.py
│  │  ├─ auth_required.py
│  │  ├─ note_rules.py
│  │  ├─ create_user.py
│  │  ├─ requirements.txt
│  │  ├─ .env.example
│  │  ├─ routes/
│  │  │  ├─ auth.py
│  │  │  ├─ events.py
│  │  │  └─ notes.py
│  │  ├─ repositories/
│  │  │  ├─ users.py
│  │  │  ├─ events.py
│  │  │  └─ notes.py
│  │  ├─ sql/
│  │  │  └─ 001_monitor.sql
│  │  └─ tests/
│  │     └─ test_api.py
│  │
│  └─ frontend/
│     ├─ index.html
│     ├─ package.json
│     ├─ package-lock.json
│     ├─ vite.config.js
│     └─ src/
│        ├─ App.jsx
│        ├─ main.jsx
│        ├─ styles.css
│        ├─ api/
│        │  ├─ client.js
│        │  ├─ auth.js
│        │  ├─ events.js
│        │  └─ notes.js
│        └─ components/
│           ├─ LoginForm.jsx
│           ├─ Dashboard.jsx
│           ├─ EventList.jsx
│           ├─ NoteList.jsx
│           ├─ NoteDetail.jsx
│           ├─ NoteForm.jsx
│           └─ DeleteConfirm.jsx
│
├─ .gitignore
├─ README.md
├─ GIT_HISTORY.md
└─ git-log.txt
```

## DB 테이블

`general/sql/001_create_posts.sql`

- `posts`: 기존 게시판 데이터

`monitor/backend/sql/001_monitor.sql`

- `monitor_users`: 운영자 아이디, 표시 이름, 비밀번호 해시
- `request_events`: 일반 서비스가 자동 전송한 method, path, status, duration, 발생 시각
- `observation_notes`: 관찰 메모 제목, 내용, 처리 상태, 생성/수정 시각

메모 처리 상태는 `확인 전`, `확인 중`, `완료` 중 하나를 DB에 저장합니다.

## 필수 기능 구현

- React 로그인 폼의 아이디·비밀번호를 state로 관리
- `POST /api/auth/login` JSON 전송
- Flask에서 PostgreSQL 운영자 계정 조회 및 비밀번호 해시 검증
- 빈 로그인 입력 `400`, 불일치 계정 `401`
- 로그인 성공 시 사용자 이름이 표시된 대시보드 전환
- 로그아웃 후 로그인 화면 복귀
- 일반 서비스 요청 기록을 PostgreSQL에 영구 저장
- `GET /api/events`로 method, path, status 표시
- 요청 기록이 없거나 조회 실패한 경우 별도 안내
- 메모 목록 `GET /api/notes`
- 메모 상세 `GET /api/notes/<id>`
- 메모 작성 `POST /api/notes`
- 메모 수정 `PUT /api/notes/<id>`
- 메모 삭제 `DELETE /api/notes/<id>`
- 작성/수정 시 서버에서 `strip()` 후 빈 값 검사, 오류 시 `400`
- 없는 메모 조회/수정/삭제 시 `404`
- 수정 취소 시 API를 호출하지 않아 기존 DB 값 유지
- 삭제 확인 화면을 열어도 삭제하지 않고, 확정할 때만 DELETE 호출
- 저장·수정·삭제 후 메모 목록 재조회
- 요청 기록/메모 전체 새로고침 버튼 제공
- React components와 api 모듈 역할 분리
- Flask routes / repositories / db 역할 분리
- SQL 사용자 입력은 `%s`와 매개변수로 전달
- 실제 `.env`는 Git에서 제외하고 `.env.example`만 제공

## 선택 과제 구현

네 가지 선택 기능을 모두 구현했습니다.

1. **요청 기록 검색·필터**
   - 경로 문자열 검색
   - HTTP 상태 코드 필터
   - 조건 해제 시 전체 목록 복귀
2. **요청 건수 요약**
   - 현재 조회 결과의 전체 요청 수
   - HTTP `400 이상`을 오류 요청으로 집계
3. **메모 처리 상태**
   - `확인 전 / 확인 중 / 완료`
   - 작성·수정 시 PostgreSQL에 저장
4. **세션 유지와 API 보호**
   - Flask session cookie 사용
   - 새로고침 시 `GET /api/auth/session`으로 로그인 상태 복원
   - 로그아웃 시 session 제거
   - 로그인하지 않은 `GET /api/events`와 모든 메모 API는 `401`
   - 일반 서비스가 기록을 보내는 `POST /api/events`만 수집용으로 로그인 없이 허용

## 환경 설정

실제 `.env`는 저장소에 포함하지 않습니다.

### general\.env

CMD에서:

```bat
cd general
copy .env.example .env
```

예시 값:

```env
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=mini_watch
DB_USER=postgres
DB_PASSWORD=자신의_PostgreSQL_비밀번호
MONITOR_URL=http://127.0.0.1:5200/api/events
```

### monitor\backend\.env

CMD에서:

```bat
cd monitor\backend
copy .env.example .env
```

예시 값:

```env
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=mini_watch
DB_USER=postgres
DB_PASSWORD=자신의_PostgreSQL_비밀번호
SESSION_SECRET=충분히_긴_임의의_문자열
```

`SESSION_SECRET`은 Flask 세션 쿠키 서명에 사용합니다.

## Windows CMD 실행 순서

아래 명령은 저장소 루트에서 시작하는 것을 기준으로 합니다.

### 1. PostgreSQL DB와 테이블 준비

PostgreSQL의 `psql` 명령을 사용할 수 있는 CMD에서:

```bat
psql -U postgres -c "CREATE DATABASE mini_watch;"
psql -U postgres -d mini_watch -f general\sql\001_create_posts.sql
psql -U postgres -d mini_watch -f monitor\backend\sql\001_monitor.sql
```

이미 `mini_watch` DB가 있으면 첫 번째 CREATE DATABASE 명령은 생략합니다.

### 2. 일반 서비스 환경 및 패키지 준비

```bat
cd general
copy .env.example .env
py -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
cd ..
```

`general\.env`의 `DB_PASSWORD`를 실제 PostgreSQL 비밀번호로 수정합니다.

### 3. 감시 API 환경 및 패키지 준비

```bat
cd monitor\backend
copy .env.example .env
py -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

`monitor\backend\.env`의 `DB_PASSWORD`와 `SESSION_SECRET`을 수정합니다.

### 4. 테스트 운영자 계정 생성

감시 API 가상환경이 활성화된 `monitor\backend` CMD에서:

```bat
python create_user.py --username admin --name "운영자"
```

비밀번호 입력 프롬프트가 나오면 테스트에 사용할 비밀번호를 입력합니다. 평문 비밀번호는 DB에 저장하지 않고 Werkzeug 해시만 `monitor_users.password_hash`에 저장합니다.

### 5. 감시 Flask API 실행 — CMD 1

```bat
cd monitor\backend
call .venv\Scripts\activate.bat
python app.py
```

접속 확인: `http://127.0.0.1:5200/health`

### 6. 일반 게시판 실행 — CMD 2

```bat
cd general
call .venv\Scripts\activate.bat
python app.py
```

게시판: `http://127.0.0.1:5100`

게시판 목록·상세와 존재하지 않는 `/board/<번호>` 등에 접속하면 요청 정보가 감시 API로 자동 전송되어 PostgreSQL에 저장됩니다.

### 7. React/Vite 실행 — CMD 3

```bat
cd monitor\frontend
npm ci
npm run dev
```

감시 화면: `http://127.0.0.1:5173`

Vite가 `/api`를 `http://127.0.0.1:5200`으로 프록시합니다.

## 통합 확인 순서

1. 일반 게시판 `http://127.0.0.1:5100`에서 게시글을 조회합니다.
2. 없는 게시글 주소에도 접속해 `404` 요청을 한 번 만듭니다.
3. `http://127.0.0.1:5173`에서 틀린 비밀번호 로그인 실패를 확인합니다.
4. 생성한 운영자 계정으로 로그인합니다.
5. 요청 기록에서 앞의 GET 경로와 상태 코드 `200/404`를 확인합니다.
6. 경로와 상태 코드 필터를 적용하고 조건 해제를 확인합니다.
7. 관찰 메모를 작성하고 목록과 상세를 확인합니다.
8. 메모 상태를 `확인 중` 또는 `완료`로 변경해 저장합니다.
9. 수정 화면에서 공백뿐인 내용으로 저장을 시도해 `400` 안내와 기존 내용 보존을 확인합니다.
10. 별도 메모를 삭제 확인 화면에서 취소해 보존되는지 확인한 뒤 삭제 확정을 확인합니다.
11. 브라우저를 새로고침해 세션과 저장된 메모가 유지되는지 확인합니다.
12. 로그아웃한 뒤 로그인 화면으로 돌아가는지 확인합니다.

## 자동 통합 검증 결과

GitHub Actions의 `Verify monitoring dashboard assignment`에서 다음을 실제로 실행해 검증합니다.

- PostgreSQL 16 서비스 시작
- 일반 게시판 SQL + 감시 SQL 적용
- Python 문법 검사
- 로그인 `400/401/200`
- 비밀번호 해시 계정 인증
- Flask session 생성·복원·로그아웃
- 미로그인 API `401`
- 이벤트 PostgreSQL 저장
- 경로/상태 필터 및 전체/오류 건수
- 메모 작성/상세/수정/삭제
- 메모 공백 입력 `400`과 기존 자료 보존
- 없는 메모 `404`
- 메모 처리 상태 DB 저장
- 기존 `general` 게시판 CRUD 유지
- 실제 일반 게시판 요청의 감시 API 수집
- `npm ci`
- Vite/React production build

## 기존 시작 자료와 이번에 구현한 부분

기존 mini-watch 단계에서 작성한 다음 기능을 시작 자료로 유지했습니다.

- `general/` Flask 게시판 CRUD
- `general/db.py`의 `connect_db()`
- 일반 서비스 요청을 감시 서비스로 보내는 `request_logging.py`

이번 과제에서 직접 확장·구현한 부분은 다음과 같습니다.

- 감시용 PostgreSQL 스키마
- 운영자 계정 생성 및 비밀번호 해시 인증
- 로그인/로그아웃/세션 API
- 요청 기록 PostgreSQL 저장·검색·필터·요약 API
- 관찰 메모 CRUD와 처리 상태 API
- API 인증 보호
- Vite + React 감시 대시보드 전체
- React components / api 모듈 분리
- 통합 테스트 및 GitHub Actions 검증

## Git 이력

구현과 구조 변경은 Git 커밋으로 관리합니다. 제출 시스템에서 `.git`이 제외돼도 확인할 수 있도록 `GIT_HISTORY.md`와 `git-log.txt`에 실제 SHA와 커밋 메시지를 함께 기록합니다.


---

## 새 과제 — Next.js 메모 앱과 GitHub Flow 협업 (2026-10-08)

기존 Flask/React 감시 대시보드는 그대로 유지하면서, **독립적인 Next.js JavaScript App Router 메모 앱**을 `next-practice/`에 추가했습니다.

- [Next.js 메모 앱 실행·구조·동작 설명](next-practice/README.md)
- [Git 민수·지윤 역할 실습, PR 3개, 작업 기록](GIT_WORK.md)
- [동작 점검표](checklist.md)
- `cd next-practice && npm ci && npm run dev`: 개발 서버 실행 (http://localhost:3000)
- `cd next-practice && npm run build && npm run start`: 프로덕션 실행

Next 메모는 **React state만** 사용하므로 새로고침하면 초기화됩니다. 기존 `monitor/frontend/`의 Flask/PostgreSQL 영구 저장 메모와는 다른, 수업 필수용 독립 앱입니다. GitHub Actions `Verify Next.js notes`에서 설치·빌드·프로덕션 홈/메모 HTTP 응답을 검증합니다.
