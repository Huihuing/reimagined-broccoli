# Mini Watch Posts CRUD

Flask, Jinja2, PostgreSQL을 사용한 게시판 CRUD 실습 과제입니다.

## 기술 스택

- Python
- Flask
- Jinja2
- PostgreSQL
- psycopg
- python-dotenv
- requests
- HTML / CSS

## 프로젝트 구조

```text
general/
├─ app.py
├─ db.py
├─ post_rules.py
├─ request_logging.py
├─ requirements.txt
├─ .env
├─ .env.example
├─ repositories/
│  ├─ __init__.py
│  └─ posts.py
├─ routes/
│  ├─ __init__.py
│  └─ posts.py
├─ templates/
│  ├─ index.html
│  ├─ detail.html
│  ├─ new.html
│  ├─ edit.html
│  ├─ delete.html
│  └─ error.html
├─ static/
│  └─ style.css
├─ sql/
│  └─ 001_create_posts.sql
└─ tests/
   └─ test_posts.py

monitor/
└─ backend/
   ├─ app.py
   └─ requirements.txt
```

## 구현 기능

- 게시글 목록: `GET /`
- 게시글 상세: `GET /board/<post_id>`
- 게시글 작성: `GET, POST /board/new`
- 게시글 수정: `GET, POST /board/<post_id>/edit`
- 게시글 삭제 확인/삭제: `GET, POST /board/<post_id>/delete`
- 공백 제거 및 빈 제목/본문 검증
- 입력 오류 `400`
- 없는 게시글 `404`
- 작성/수정/삭제 후 `303` 리다이렉트
- PostgreSQL `posts` 테이블과 시퀀스 사용
- `INSERT ... RETURNING id`
- Blueprint / Repository / Validation / Request Logging 역할 분리
- 일반 서비스 요청 로그를 `requests`로 감시 서비스에 JSON 전송

## 실행

### 1. PostgreSQL 준비

`general/.env`의 DB 접속 정보를 자신의 PostgreSQL 환경에 맞게 수정합니다.

```env
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=mini_watch
DB_USER=postgres
DB_PASSWORD=postgres
MONITOR_URL=http://127.0.0.1:5200/api/events
```

`general/sql/001_create_posts.sql`을 실행하여 `posts` 테이블과 시퀀스를 준비합니다.

### 2. 감시 서비스

```bash
cd monitor/backend
python -m venv .venv
pip install -r requirements.txt
python app.py
```

### 3. 게시판 서비스

```bash
cd general
python -m venv .venv
pip install -r requirements.txt
python app.py
```

게시판은 기본적으로 `http://127.0.0.1:5100`, 감시 서비스는 `http://127.0.0.1:5200`에서 실행됩니다.

## 자동 검증

GitHub Actions의 `Verify posts CRUD assignment`에서 PostgreSQL 16을 실제로 실행하여 다음을 확인합니다.

- Python 문법
- posts 테이블 및 시퀀스 준비
- 목록 / 상세 / 작성 / 수정 / 삭제
- 400 / 404 / 303 응답
- 잘못된 입력 시 DB 유지
- 삭제 확인 GET에서 데이터 보존
- 삭제 후 상세·수정·삭제 URL 404
- 요청 로그의 감시 서비스 JSON 수집


## Git 커밋 이력

구현과 구조 변경은 Git 커밋으로 관리했습니다. 제출 환경에서 `.git` 디렉터리가 제외되더라도
커밋 이력을 확인할 수 있도록 루트의 [GIT_HISTORY.md](./GIT_HISTORY.md)와
[git-log.txt](./git-log.txt)에 실제 commit SHA와 메시지를 함께 기록했습니다.

주요 게시판 작업 커밋:

```text
76e9c733 feat: implement Flask PostgreSQL posts CRUD
7f3a3a6e test: cover posts CRUD requirements
fdccf71e ci: verify Flask PostgreSQL posts CRUD
6a434bb0 feat: switch main to posts CRUD assignment
```
