# reimagined-broccoli

회원가입 구현 과제용 프로젝트입니다.

## 기술 스택

- Frontend: Next.js + TypeScript
- Backend: Python + FastAPI
- ORM: SQLAlchemy
- Database: SQLite
- Password protection: bcrypt one-way hashing

## 구현된 요구사항

- Python 백엔드
- SQLAlchemy ORM 기반 `users` 테이블 저장
- 비밀번호 평문 저장 금지: bcrypt 해시만 `password_hash`에 저장
- Next.js 회원가입 화면
- 중복 아이디/이메일 검사
- frontend/backend 및 model/schema/router/service 모듈 분리

## 디렉토리

```text
backend/
  app/
    models/
    routers/
    schemas/
    services/
    database.py
    main.py
frontend/
  app/
    signup/
```

## 실행 방법

### Backend

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

백엔드는 기본적으로 `http://localhost:8000`에서 실행됩니다.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

프론트엔드는 기본적으로 `http://localhost:3000`에서 실행됩니다.

다른 백엔드 주소를 사용하려면 frontend의 환경변수 `NEXT_PUBLIC_API_URL`을 설정합니다.

## 회원가입 API

`POST /api/auth/signup`

요청 예시:

```json
{
  "username": "broccoli_user",
  "email": "user@example.com",
  "password": "password123"
}
```

성공하면 사용자 id, username, email, created_at만 반환하며 비밀번호와 password_hash는 응답하지 않습니다.
