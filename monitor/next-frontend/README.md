# Next.js → Flask API → PostgreSQL 메모 (심화 3·4)

기존 `monitor/backend` Flask API의 데이터를 Next.js에서 직접 소비하는 독립 화면입니다. **기존 `next-practice`는 React state만 사용하며 새로고침 시 초기화되지만, 이 화면은 PostgreSQL에 영구 저장됩니다.**

## 실제 구현

- 인증: `POST /api/auth/login`, `GET /api/auth/session`, `POST /api/auth/logout`
- 목록: `GET /api/notes` / 상세: `GET /api/notes/:id`
- 등록: `POST /api/notes` → PostgreSQL `observation_notes` → GET 상세 재조회
- 수정: `PUT /api/notes/:id` → DB 반영 및 재조회. **수정 취소에는 PUT 요청 없음**
- 삭제: 확인 창 → `DELETE /api/notes/:id` → 목록 재조회. **삭제 취소에는 DELETE 없음**
- 제목 또는 본문이 공백뿐이면 클라이언트 검증 메시지 출력. Flask도 별도로 `400` 오류 반환
- 삭제된 ID 등 존재하지 않는 자료에 GET/PUT/DELETE 요청하면 Flask `404` 반환. Next.js는 성공 메시지 대신 HTTP 상태와 오류 안내를 표시하고 입력 내용 보존
- 새로고침 후에도 Flask 로그인 세션 및 PostgreSQL에서 조회한 메모 유지

**구조:** 브라우저는 동일 출처 `/api/*` 경로로 요청하고, `next.config.mjs`의 rewrite가 `FLASK_API_URL`(기본 localhost:5200)의 기존 Flask API로 전달합니다. 데이터베이스 자격정보는 Next.js에 넘기지 않으며 브라우저에서 DB를 직접 열지 않습니다. 인증은 Flask HttpOnly session cookie 방식입니다.

## 필요한 환경

- Node.js 22 이상 권장
- Python 3.12+, PostgreSQL 16
- 설치된 `monitor/backend/requirements.txt`
- `FLASK_API_URL`은 백엔드 서버만 가리키며 `.env`에 비밀번호를 저장하지 않습니다. 실제 `.env`는 제출 제외

### 1. DB 준비 (기존 SQL 그대로 사용)

이 저장소에 포함된 **[DB 준비 SQL](../backend/sql/001_monitor.sql)** 파일을 사용합니다. `mini_watch` DB는 기존 실습에서 쓰던 것을 재사용할 수 있습니다.

```powershell
# 저장소 루트에서, PostgreSQL이 실행 중일 때
psql -U postgres -c "CREATE DATABASE mini_watch;"
psql -U postgres -d mini_watch -f monitor/backend/sql/001_monitor.sql
```

DB가 이미 있으면 CREATE DATABASE는 건너뜁니다.

### 2. Flask 백엔드 시작 (PowerShell 1)

```powershell
cd monitor/backend
Copy-Item .env.example .env
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
# .env의 DB_PASSWORD, SESSION_SECRET을 본인의 값으로 수정
.\.venv\Scripts\python.exe create_user.py --username admin --name "운영자"
.\.venv\Scripts\python.exe app.py
```

계정 생성 도구가 비밀번호를 물으면 실습용 비밀번호를 입력합니다. Flask 상태 확인: http://127.0.0.1:5200/health

### 3. Next.js 화면 시작 (PowerShell 2)

```powershell
cd monitor/next-frontend
Copy-Item .env.example .env.local
npm ci
npm run dev
```

http://localhost:3001 접속 후 앞서 생성한 운영자 계정으로 로그인합니다. 환경 설정 `FLASK_API_URL=http://127.0.0.1:5200`이 기본입니다.

### 4. 프로덕션 빌드·실행

개발 서버를 종료한 후:

```powershell
npm run build
npm run start
```

기본 실행 포트는 3001입니다. 기존 `next-practice`의 3000번 포트와 충돌하지 않습니다.

## 수동 점검 순서

1. 로그인 없이 메모 API 요청 → 401. 올바른 계정 로그인 → 목록과 사용자 표시
2. 메모 제목·내용·상태를 입력해 등록하고 목록에서 선택 → 상세 GET
3. F5 새로고침 후 목록에 등록 메모가 그대로 있는지 확인
4. 수정 시작·수정 취소 → 원본 유지
5. 공백 저장 시 안내·원본 유지 및 직접 빈 본문 PUT → HTTP 400
6. 수정 저장 후 F5 → 변경된 본문과 처리 상태 유지
7. 삭제 확인 창에서 취소 → 원본 유지, 확정 → DB 삭제 및 목록에서 제거
8. 삭제 후 F5 → 해당 메모가 다시 나타나지 않음
9. 삭제된 ID에 GET/PUT/DELETE 요청 → HTTP 404, 화면은 성공으로 표시하지 않음
10. 수정 중인 메모가 다른 요청으로 제거된 상태에서 저장하면 HTTP 404 안내, 성공 메시지 없음

## 자동화 검증

`npm run test:e2e`는 설치된 Playwright Chromium으로 Next.js 브라우저 동작을 확인합니다. 테스트용 Flask+PostgreSQL 실행 환경이 필요합니다. GitHub Actions [Verify Next Flask PostgreSQL CRUD](https://github.com/Huihuing/reimagined-broccoli/actions/workflows/next-flask-db.yml)는 PostgreSQL 16, Flask 세션 인증 계정과 API, Next.js 프로덕션 빌드, Chromium 브라우저 테스트를 연동합니다.

실제 테스트 결과는 CI 로그로 판단합니다. 제공한 Python/SQL/Node 설정에서 생성하는 DB 계정 비밀번호는 예제·CI 테스트 환경 전용이며 실제 비밀키는 커밋하지 않습니다.
