# Git Commit History Evidence

이 프로젝트는 Git/GitHub으로 구현과 구조 변경 이력을 관리합니다.

Repository: https://github.com/Huihuing/reimagined-broccoli  
Branch: `main`

제출 시스템이 소스 파일만 전달하고 `.git` 디렉터리를 제외하는 경우에도 실제 커밋 이력과 메시지를 확인할 수 있도록 주요 이력을 기록합니다.

## 기존 게시판 단계

```text
76e9c7331d7f6aba77bea1af0c1d165baacc7c99 feat: implement Flask PostgreSQL posts CRUD
7f3a3a6ec8ceb7b44efaade72e2ce0cc533e1bf4 test: cover posts CRUD requirements
fdccf71efa0826c3c30484cdf21a0153619dbe4c ci: verify Flask PostgreSQL posts CRUD
6a434bb07b1116dc3313dc20cbb4ccfb77fbccbf feat: switch main to posts CRUD assignment
0c705557083719672bb8ef7e4a73de3bb2112305 docs: add Git commit history evidence
```

## React + Flask 감시 대시보드 단계

```text
9e040e9451f5917dfb8444b7d946a4b39369e83a feat: build React Flask monitoring dashboard
d38d9b2c763cb9ecc435eb045ae4786167ca110e ci: verify React Flask monitoring dashboard
047ed052ae28d4de52bc84c060c9e66543729ec0 chore: add monitor frontend package lock
```

### 커밋별 작업

- `feat: build React Flask monitoring dashboard`
  - `monitor/backend`를 PostgreSQL 기반 Flask API로 확장
  - 운영자 로그인 및 비밀번호 해시 검증
  - request event 영구 저장
  - 관찰 메모 CRUD와 상태 저장
  - Flask session과 API 보호
  - `monitor/frontend` Vite + React 화면 및 역할별 컴포넌트/API 모듈 추가
  - 실제 `.env` 제거 및 `.env.example` 구성
- `ci: verify React Flask monitoring dashboard`
  - PostgreSQL 16을 실제 실행하는 통합 검증 구성
  - 기존 general 게시판과 monitor 수집 연동 확인
  - 로그인/세션/이벤트/메모 API와 React production build 검증
- `chore: add monitor frontend package lock`
  - 실제 npm 설치 결과로 생성된 `monitor/frontend/package-lock.json` 추가

## 확인 방법

Git 저장소를 clone한 경우:

```bash
git log --oneline --decorate
```

GitHub 저장소의 Commit history에서도 같은 SHA와 메시지를 확인할 수 있습니다.
