# Day2 클라우드 배포·DB·오류 수집 작업 기록

> 프로젝트: https://github.com/Huihuing/reimagined-broccoli  
> 기준 코드: `18bb1c76aeab2bebef4c522a760807e0910f5f70` (`main` 시작점)  
> 작업 브랜치: `day2-deploy`  
> 현재 상태: **코드 및 CI 검증 대상 준비**, 실제 Render/Supabase/Sentry 계정 배포 **미완료**. 실제 URL과 비밀번호를 제출하지 않아도 되는 과제 조건을 따름.

## 1. 기존 프로젝트와 세 앱

기존 `general/`은 Flask 게시판(목록/상세/등록/수정/삭제)이며, `monitor/backend/`은 Flask 운영자 인증·기록·관찰 메모 API다. `monitor/next-frontend/`은 기존 Flask API로 메모를 영구 저장하는 **실제 Next.js App Router UI**다. 별도 연습용 `next-practice/`와 기존 `monitor/frontend/` Vite/React는 삭제하거나 Next 대신 제출하지 않는다. 두 Compose, Nginx 게이트웨이는 Day2에 **로컬용으로 새로 추가**했다. Render에서는 아래 세 Dockerfile을 각각 직접 사용한다.

| 앱 | Render Root Directory | Dockerfile / Build Context | Health Check | Branch | 상태 |
| --- | --- | --- | --- | --- | --- |
| 감시 Flask API | `monitor/backend` | `./Dockerfile` / `.` | `/health` | `day2-deploy` | 미배포 |
| 일반 Flask | `general` | `./Dockerfile` / `.` | `/health` | `day2-deploy` | 미배포 |
| 감시 Next.js | `monitor/next-frontend` | `./Dockerfile` / `.` | `/` | `day2-deploy` | 미배포 |

Render 설정: Docker Web Service, Hobby/Free(이용 가능한 경우), Docker Command는 **빈칸**(Dockerfile CMD 사용), Auto-Deploy **On Commit**. Flask 두 컨테이너는 `waitress-serve --host=0.0.0.0 --port=$PORT app:app`; 개발 실행 `python app.py`는 유지한다. Next는 잠금 파일 `package-lock.json` 기준 `npm ci`, `npm run build` 뒤 `next start --hostname 0.0.0.0 -p $PORT`로 시작한다. 빌드에서는 API/DB 요청을 하지 않고 클라이언트의 실행 시점에 요청한다.

Render 설정 문서: https://render.com/docs/web-services. 서버 프로세스는 `0.0.0.0` 및 Render의 `PORT`를 사용한다. /health는 **프로세스 생존 확인**이며 DB 접속·로그인이나 기록 저장 성공을 증명하지 않는다. DB 점검은 실제 API 로그인·조회/저장으로 따로 한다.

## 2. Supabase 분리 및 배포 SQL

실제 서비스에서는 일반과 감시에 **서로 다른 Supabase 프로젝트**를 사용해야 한다. 일반 서비스 DB와 감시 서비스 DB가 같은 `postgres` DB_NAME을 써도, 프로젝트 참조가 다르면 다른 저장소다. 기존 DB 삭제나 테이블 초기화를 수행하지 않는다.

| 변수 | 일반 Flask | 감시 Flask |
| --- | --- | --- |
| `DB_HOST` | 일반 Supabase Session pooler host | 별도 감시 Supabase Session pooler host |
| `DB_PORT` | `5432` | `5432` |
| `DB_NAME` | `postgres` | `postgres` |
| `DB_USER` | 일반 프로젝트의 `postgres.<project-ref>` | 감시 프로젝트의 `postgres.<project-ref>` |
| `DB_PASSWORD` | 일반 프로젝트 비밀번호 (Render 서버 비밀 설정) | 감시 프로젝트 비밀번호 (별도 비밀) |
| `DB_SSLMODE` | `require` | `require` |

위 값은 Dashboard → Connect → Session pooler에서 복사한다. `DB_SSLMODE=prefer`은 로컬 PostgreSQL 실습용이다. 외부 Supabase에서는 반드시 `require`로 설정한다. `.env.example`은 로컬 기본값이므로 그대로 클라우드에 복사하지 않는다. Supabase는 Python psycopg의 DB 직접 연결만 사용하며 수업 조건에 따라 Data API를 비활성화한다. 웹 프런트에 Supabase DB 비밀번호를 노출하지 않는다.

**일반 DB에만** `general/sql/deploy.sql` 실행: `posts`와 `users` 생성. **감시 DB에만** `monitor/backend/sql/deploy.sql` 실행: 기존 `monitor_users`, `request_events`, `observation_notes`을 비파괴 `CREATE TABLE IF NOT EXISTS`로 구성하고 `event_type` 열만 있지 않으면 추가. 이 프로젝트의 원래 테이블명은 과제 예시의 감시 `users` / `http_events` / `notes`에 각각 **대응되는 실제 DB 테이블**이다. 기존 Flask `repositories/users.py`, `repositories/events.py`, `repositories/notes.py`가 해당 실제 테이블에서 데이터를 읽고 쓴다. 이름만 바꾸느라 원래 게시글·메모나 실행중인 코드가 망가지지 않도록 유지했다. `general/repositories/posts.py`의 원래 CRUD도 동일하게 유지했다.

Supabase 연결 문서: https://supabase.com/docs/guides/database/connecting-to-postgres. 데이터는 Render 재배포 이후에도 각 외부 DB에 남도록 설계됐으며, **실제 외부 DB 검증은 아직 수행하지 않았다**.

### 계정 준비 (각 Flask 폴더, Windows CMD)

실제 운영 비밀번호는 커밋하지 않는다. Python 3.12+를 사용한다. 계정은 **해당 `.env`가 연결하는 DB**에 생성된다.

```cmd
cd general
py -m venv .venv
call .venv\Scripts\activate.bat
pip install -r requirements.txt
copy .env.example .env
REM 실제 일반 프로젝트 DB 및 SECRET_KEY 등을 .env에 편집한다
python create_user.py --username student
deactivate

cd ..\monitor\backend
py -m venv .venv
call .venv\Scripts\activate.bat
pip install -r requirements.txt
copy .env.example .env
REM 실제 감시 프로젝트 DB 및 SECRET_KEY 등을 .env에 편집한다
python create_user.py --username operator --name "운영자"
deactivate
```

두 스크립트 모두 `werkzeug.security.generate_password_hash`로 해시를 각 DB의 `users` / `monitor_users`에 저장한다. 일반 생성 스크립트는 새 12자 이상 비밀번호를 두 번 받고, 감시 생성 스크립트는 터미널에서 `getpass` 입력을 받는다. 기존 감시 스크립트의 `--password` 테스트 옵션은 CI 호환을 위해 유지하지만 실제 운영에서는 명령행에 비밀번호를 넣지 않는다. Render Free에는 Shell이 없을 수 있으므로 앱 서비스 내부에서 초기 계정을 만든다고 가정하지 않는다.

## 3. 주소·토큰·쿠키·로그인 흐름

```text
브라우저 -> 일반 Flask /api/auth/login -> 일반 users DB
  -> general/request_logging.py -> HTTPS MONITOR_URL + X-Event-Token
  -> 감시 Flask /api/events -> request_events DB
브라우저 -> 감시 Next.js 같은 출처 /api/*
  -> Next 서버 Route Handler (MONITOR_API_URL)
  -> 감시 Flask /api/auth/*, /api/events, /api/notes -> 감시 DB
```

- 일반의 `MONITOR_URL`은 `https://<감시-flask>.onrender.com/api/events`; 감시 서버의 `EVENT_TOKEN`과 일반 서버의 `EVENT_TOKEN`은 동일한 **비밀값**이다. 감시 이벤트 수신은 헤더 `X-Event-Token`을 상수 시간 비교하며 누락되면 503, 불일치면 401이다. Next는 POST `/api/events`를 노출하지 않는다.
- 감시 Next의 서버 환경 `MONITOR_API_URL`은 `https://<감시-flask>.onrender.com` **(/api 없는 기준 주소)**. 기존 개발용 `FLASK_API_URL`도 호환 가능하지만 `MONITOR_API_URL`이 우선한다.
- 브라우저의 `lib/api.js`는 같은 출처 `/api`를 호출한다. `app/api/[...path]/route.js`는 요청 Cookie·X-CSRF-Token 및 요청 본문, 응답 Set-Cookie·status를 전달한다. 설정 오류/타임아웃이면 502 안내 JSON, 알 수 없는 API는 404. 감시 화면의 오류 메시지와 기록 다시 불러오기 버튼으로 복구한다.
- 감시 로그는 `event_type`을 PostgreSQL에 저장한다. 일반의 `/api/auth/login`에 대해 HTTP 401이면 `login_failure`, 200이면 `login_success`, 나머지는 `http_request`. 감시 Next의 **요청 기록** 표에 유형·경로·상태 코드를 표시한다. 기존 React/Vite 감시 화면과 게시판·메모 CRUD는 보존했다.
- Flask 둘 다 `SECRET_KEY`와 `SESSION_COOKIE_SECURE`를 환경에서 읽는다. 서비스별 **서로 다른** 고유 세션 키를 생성한다. 개발용 HTTP는 `SESSION_COOKIE_SECURE=false`, Render HTTPS는 `true`. 모니터의 과거 `SESSION_SECRET` 변수도 호환한다. DB 비밀번호·SECRET_KEY·EVENT_TOKEN·SENTRY_DSN은 서버 환경에만 두며 `NEXT_PUBLIC_*`에 저장하지 않는다.

로컬 Compose (`compose-general.yaml`, `compose-monitor.yaml`)은 별도 Postgres와 영속 볼륨·로컬 nginx 8081/8082·공통 `rb-events` 네트워크를 쓴다. 서버가 없으면 아래처럼 수동 네트워크를 만들고 감시부터 시작한다. 개발 토큰과 비밀번호는 샘플이며 **외부 서버에 절대 재사용하지 않는다**.

```bash
docker network create rb-events
docker compose -f compose-monitor.yaml up -d --build
docker compose -f compose-general.yaml up -d --build
# 일반 http://127.0.0.1:8081 / 감시 http://127.0.0.1:8082
```

각 Compose의 `down`은 `-v` 없이 수행해 볼륨을 유지한다. 실제 Render는 이 두 Compose가 아니라 앱별 Dockerfile을 사용한다.

## 4. Sentry와 실습 오류 수정

두 Flask의 의존성은 `sentry-sdk[flask]`를 포함한다. `app.py`에서 `configure_errors('mini-general')` / `configure_errors('mini-monitor')`를 앱 로딩 시 호출하므로 `python app.py`와 Waitress의 `app:app` 모두에 적용된다. `SENTRY_DSN`을 비워도 앱은 정상 실행된다. `SENTRY_ENVIRONMENT`는 각각 `mini-general`, `mini-monitor`, `APP_VERSION`은 배포 커밋이나 버전으로 설정한다.

`observability.py`의 `before_send`는 요청 `data`·`cookies`·`headers`·`query_string`, 최상위 `user`를 제거한다. `send_default_pii=False`, `include_local_variables=False`, `max_request_body_size=never`, traces 0 설정도 유지한다. 이러한 설정은 데이터 최소화 조치이며 절대적 비수집 보장은 아니다.

수업 **starter**의 `general/app.py::sentry_test()`에는 `result = 1 / 0` (ZeroDivisionError)가 있다. 이 본인 저장소에는 원래 해당 실습 경로가 없었으므로 오류를 새로 도입하지 않고 안전하게 추가했다. 이번 `general/app.py`에서는 `return jsonify({'result': 1, 'status': 'ok'})`으로 200 JSON 응답한다. `ENABLE_SENTRY_TEST=true` 및 일반 로그인 모두 만족해야 접근 가능하다. 기본 예시는 `false`이며 검증 후 **반드시 false로 복귀**한다.

코드 비교 (강사 제공 starter → 적용 코드):

```diff
- result = 1 / 0
- return {'result': result}
+ return jsonify({'result': 1, 'status': 'ok'})
```

수정 파일: `general/app.py` (수정 커밋 `70a7da4b8737`), `monitor/backend/app.py` (수정 커밋 `6bd482549939`). 기준 프로젝트 커밋: `18bb1c76aeab2bebef4c522a760807e0910f5f70`. 수업 starter 오류와 대비한 diff이므로 **본인 기존 커밋에 오류가 있었던 것처럼 주장하지 않는다**. Sentry 화면에서 이슈 Resolve를 눌러도 코드가 수정되거나 재배포되는 것이 아니다. 이번 실제 Sentry 수신 확인은 미완료다.

## 5. 실제 배포·검증 순서와 장애 진단

1. `day2-deploy` 브랜치의 소스·Dockerfile·`.env.example`·`deploy.sql`을 push한 후 두 Supabase 프로젝트 준비, 비파괴 SQL 실행, 로컬 Python 가상환경에서 `create_user.py`로 계정 생성.
2. Render 감시 Flask Docker Web Service 생성: DB_* 6개 + `SECRET_KEY`, `SESSION_COOKIE_SECURE=true`, `EVENT_TOKEN`, `ENABLE_SENTRY_TEST=false`, Sentry 선택 변수 지정. `/health` 200과 실제 계정 로그인/DB 접근을 **각각** 확인.
3. 일반 Flask 배포: 일반 DB 설정 + 다른 SECRET_KEY + 같은 EVENT_TOKEN + `MONITOR_URL=<감시 URL>/api/events`. 감시 Next 배포: `MONITOR_API_URL=<감시 API 기준 URL>`. Render의 Published Deploy Commit이 최신 코드와 일치하는지 확인.
4. 일반에서 로그인 비밀번호 실패(401), 성공(200)을 만들고 감시 Next에서 로그인 후 **요청 기록 불러오기** → 두 이벤트 유형 확인. 게시글/메모 CRUD 및 새로고침 후 조회, 두 Supabase 프로젝트에서 해당 행 확인.
5. 새 수정 커밋을 `git push` → Render On Commit 재배포 → 배포 커밋 확인 → 기존 게시글·메모 영구 유지 확인. 실습 오류 경로는 켠 뒤 200 확인하고 `ENABLE_SENTRY_TEST=false`로 끈다.

오류별 점검:

| 증상 | 앱/코드 | 먼저 확인할 항목 |
| --- | --- | --- |
| 감시 API 주소 오류/502 | Next `app/api/[...path]/route.js`; 일반 `request_logging.py` | Next `MONITOR_API_URL`, 일반 `MONITOR_URL`, 감시 /health, Render 요청·경고 로그 |
| 이벤트 미전송/401 | 감시 `routes/events.py` | 양쪽 `EVENT_TOKEN`이 동일하고 비밀이 유효한지, `X-Event-Token` 헤더 |
| DB 접속/SSL 오류 | 각각 `db.py`, Flask logs | 두 프로젝트의 Host/User/Port/Password, `DB_SSLMODE=require`, SQL Editor와 Session pooler |
| 입력 오류/400 | Flask auth/notes/posts route | 빈 JSON/폼, 유효성 규칙, API 400/404와 네트워크 502를 구분 |
| 감시 화면 오류 | Next `lib/api.js`, `components/DatabaseNotes.jsx`와 `EventList.jsx` | JSON `error` 표시와 다시 불러오기, 쿠키/CSRF 전달, 로그인 여부 |

`/health`는 위와 별개로 DB 접속을 보장하지 않는다. 로그인·메모의 실제 저장 성공을 보아야 한다.

## 6. 변경 이력 및 제출 범위

기존 시작 코드: 일반 Flask/PostgreSQL 게시판, 감시 Flask + 기존 React/Vite, 별도 Next 메모 UI. 직접 변경한 것: 두 Flask DB SSL·배포 설정·Sentry, 일반 로그인 및 계정 생성, 이벤트 인증·분류·DB 열, Next 런타임 프록시·이벤트 UI, 앱 Dockerfile, 별도 Compose·게이트웨이, 배포 SQL·.env.example, 테스트, 이 문서와 README. 원래 프로젝트의 학습·Git 협업 파일은 삭제하지 않았다.

기준 커밋: `18bb1c76aeab2bebef4c522a760807e0910f5f70`. 개별 변경 SHA는 `day2-deploy` 커밋 히스토리에 있으며 문서 내 주요 Sentry 수정 커밋을 위에 적었다. Classroom에서는 이 브랜치가 포함된 GitHub URL 또는 코드 ZIP을 제출한다. **실제 배포 URL·Sentry 수신 증거가 없다고 해서 미확인 작업을 완료로 쓰지 않는다.** .env와 DB 비밀값, node_modules, .next, 가상환경을 제출하지 않는다.
