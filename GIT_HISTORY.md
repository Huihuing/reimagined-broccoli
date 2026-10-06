# Git Commit History Evidence

이 프로젝트는 Git/GitHub으로 구현 및 구조 변경 이력을 관리했습니다.

Repository: https://github.com/Huihuing/reimagined-broccoli  
Branch: `main`

제출 시스템이 소스 파일만 전달하고 `.git` 디렉터리를 포함하지 않는 경우에도
실제 Git 커밋 이력과 커밋 메시지를 확인할 수 있도록 아래에 기록합니다.

## 게시판 CRUD 구현 관련 실제 커밋

```text
76e9c7331d7f6aba77bea1af0c1d165baacc7c99 feat: implement Flask PostgreSQL posts CRUD
7f3a3a6ec8ceb7b44efaade72e2ce0cc533e1bf4 test: cover posts CRUD requirements
fdccf71efa0826c3c30484cdf21a0153619dbe4c ci: verify Flask PostgreSQL posts CRUD
6a434bb07b1116dc3313dc20cbb4ccfb77fbccbf feat: switch main to posts CRUD assignment
```

각 커밋의 역할은 다음과 같습니다.

- `feat: implement Flask PostgreSQL posts CRUD`
  - Flask/Jinja2/PostgreSQL 게시판 CRUD 구현
  - `general/app.py`, `db.py`, `post_rules.py`
  - `repositories/posts.py`, `routes/posts.py`
  - templates, static CSS, SQL, request logging, monitor 서비스 추가
- `test: cover posts CRUD requirements`
  - 목록/상세/작성/수정/삭제 테스트 추가
  - 400/404/303 응답과 잘못된 입력 시 DB 보존 검증
- `ci: verify Flask PostgreSQL posts CRUD`
  - PostgreSQL을 실제 실행하는 GitHub Actions 검증 추가
  - 감시 서비스 요청 로그 수집 검증 추가
- `feat: switch main to posts CRUD assignment`
  - 게시판 과제 제출용으로 프로젝트 구조를 정리
  - `general/`과 `monitor/backend/` 중심 구조로 분리

GitHub 저장소의 commit history에서도 동일한 SHA와 메시지를 확인할 수 있습니다.

## 확인 명령

Git 저장소를 clone한 경우 다음 명령으로 같은 이력을 확인할 수 있습니다.

```bash
git log --oneline --decorate
```

이 문서 자체도 Git으로 커밋되어 관리됩니다.
