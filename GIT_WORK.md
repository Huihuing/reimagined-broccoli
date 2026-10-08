# GitHub Flow 협업 작업 기록 — 민수 / 지윤

저장소: https://github.com/Huihuing/reimagined-broccoli  
방식: `main` + `feature/*` 작업 브랜치 → Pull Request 자체 검토 → **Create a merge commit** → main 동기화  
사용 계정: `Huihuing` (하나의 GitHub 계정으로 민수·지윤 역할 분리)

## 1. GitHub에서 실제 완료한 작업과 증빙

| 역할 | 작업 브랜치 | PR / base | 실제 변경 파일 | 검토 및 merge commit |
| --- | --- | --- | --- | --- |
| 민수 | `feature/minsu` | [PR #1](https://github.com/Huihuing/reimagined-broccoli/pull/1) → `main` | `minsu.md` | PR 생성 뒤 추가 커밋 `1b3b4a172207cf0430d1bdc0d3298cb6c775423d` 반영, `c482ac5911cd9942a7db2932b018d8ab2364e0ab` |
| 지윤 | `feature/jiyun` | [PR #2](https://github.com/Huihuing/reimagined-broccoli/pull/2) → `main` | `jiyun.md` | `4542b3faf8a7213998ec67598df64b95dd070443` |
| 협동 점검 | `feature/checklist` | [PR #3](https://github.com/Huihuing/reimagined-broccoli/pull/3) → `main` | `checklist.md` | 최신 main에서 새 분기 생성, `f4273d9df2f8aa017fae5cefa4fda4de22dc43dd` |

세 PR은 모두 GitHub API에서 `merged: true`를 반환했으며 각각 **merge method: merge**로 실행했습니다. PR Conversation에서 변경 파일과 기존 소스 영향 여부를 직접 검토한 댓글을 확인할 수 있습니다. 자기 PR에 대한 Approve는 사용하지 않았습니다.

### PR 생성 뒤 보완 커밋

1. 민수 브랜치 `34ee9fd490170d9a16d39f937460fb27e4d884ad`로 최초 PR #1 생성
2. 동일 `feature/minsu`에 `1b3b4a172207cf0430d1bdc0d3298cb6c775423d` 추가
3. PR #1은 새 PR 없이 자동으로 변경되어 총 커밋 2개
4. `Files changed` 검토 결과 `minsu.md`만 포함, PR #2는 `jiyun.md`만 포함, PR #3은 `checklist.md`만 포함
5. PR #1 → PR #2 → PR #3 순으로 실제 merge commit 방식 병합

## 2. 두 로컬 폴더의 재현 명령

**아래는 사용자 PC에서 실행할 명령 예시입니다. 실제 실행·출력을 수집하기 전까지 PC에서 clone / checkout / merge / pull을 수행했다고 주장하지 않습니다.** 이 저장소의 원격 PR은 이미 병합된 상태이므로 당시의 분기 시작점 `81f30c7a55c85e300d8bfaebfd214a37f163d660`을 기준으로 로컬 merge 흐름을 재현할 수 있습니다.

PowerShell에서 동일 부모 폴더에서 실행:

```powershell
git clone https://github.com/Huihuing/reimagined-broccoli.git git-practice-minsu
git clone https://github.com/Huihuing/reimagined-broccoli.git git-practice-jiyun
git -C git-practice-minsu remote -v
git -C git-practice-jiyun remote -v
```

두 `origin` 모두 `https://github.com/Huihuing/reimagined-broccoli.git`여야 합니다.

### 민수 폴더의 작업 브랜치와 main 방향

```powershell
cd git-practice-minsu
git switch -c replay/minsu-base 81f30c7a55c85e300d8bfaebfd214a37f163d660
git switch -c replay/minsu-work origin/feature/minsu
git diff replay/minsu-base..replay/minsu-work -- minsu.md
git switch replay/minsu-base
git merge --ff-only replay/minsu-work
git log -2 --oneline
git switch main
git pull --ff-only origin main
Get-Content minsu.md
Get-Content jiyun.md
git branch -d replay/minsu-work replay/minsu-base
```

위 재현에서 `replay/minsu-base`가 **수신 브랜치**이며 `replay/minsu-work`의 커밋이 여기에 들어옵니다. 실제 수업 예시 `main`에서 `git merge feature/minsu` 실행도 동일한 방향입니다. 이미 원격 main에 merge된 상태에서는 `Already up to date.`가 나올 수 있어 역사적 시작점을 재현 브랜치로 분리했습니다.

### 지윤 폴더의 작업 브랜치와 main 방향

```powershell
cd ..\git-practice-jiyun
git switch -c replay/jiyun-base 81f30c7a55c85e300d8bfaebfd214a37f163d660
git switch -c replay/jiyun-work origin/feature/jiyun
git diff replay/jiyun-base..replay/jiyun-work -- jiyun.md
git switch replay/jiyun-base
git merge --ff-only replay/jiyun-work
git switch main
git pull --ff-only origin main
Get-Content minsu.md
Get-Content jiyun.md
Get-Content checklist.md
git branch -d replay/jiyun-work replay/jiyun-base
```

작업 완료 후 각각의 폴더에서 생성한 로컬 역할 브랜치는 main에 병합된 뒤 `git branch -d <브랜치명>`으로 정리합니다. 원격 작업 브랜치는 PR 추적을 위해 유지합니다.

## 3. 실제 출력 기록: GitHub 원격 응답

```text
PR #1: merged=true, merge commit c482ac5911cd9942a7db2932b018d8ab2364e0ab
PR #2: merged=true, merge commit 4542b3faf8a7213998ec67598df64b95dd070443
PR #3: merged=true, merge commit f4273d9df2f8aa017fae5cefa4fda4de22dc43dd
PR #1 Files changed: minsu.md
PR #2 Files changed: jiyun.md
PR #3 Files changed: checklist.md
PR #1 initial commit 34ee9fd490170d9a16d39f937460fb27e4d884ad
PR #1 follow-up commit 1b3b4a172207cf0430d1bdc0d3298cb6c775423d
```

**실제 로컬 명령 출력:** 아직 사용자 PC에서 수집되지 않았음. 두 폴더에서 `remote -v`, `git branch -av`, `git diff`, `git merge`, `git pull`, `git log --graph --oneline` 출력을 별도로 캡처해서 이 문서에 추가하면 1~8번 실습 검증이 완성됩니다. 위 재현 명령의 결과를 실제 출력으로 복사하기 전에는 완료라고 표시하면 안 됩니다.

## 4. 핵심 질문

**Q. main에서 `git merge feature/minsu`를 실행하면 어느 브랜치가 변경을 받는가?**  
현재 체크아웃한 `main`이 `feature/minsu`의 변경을 받습니다. 작업 브랜치는 merge 명령으로 변경되지 않습니다.

**Q. GitHub에서 PR을 병합한 뒤에도 각 폴더에서 pull해야 하는 이유는 무엇인가?**  
GitHub의 원격 `main`만 갱신되고 각 폴더의 로컬 `main`은 자동으로 갱신되지 않기 때문입니다. 각 폴더에서 `git pull`로 최신 merge commit을 내려받아야 두 파일을 함께 확인할 수 있습니다.

## 5. Next.js 앱 변경 기록

필수 메모 앱 소스: [next-practice/](https://github.com/Huihuing/reimagined-broccoli/tree/main/next-practice)  
구현: `app/layout.js`, `app/page.js`, `app/notes/page.js`, `components/Counter.js`, `components/Notes.js`, `app/globals.css`.  
앱 생성·빌드·실행 확인은 [next-practice/README.md](next-practice/README.md) 및 GitHub Actions `Verify Next.js notes` 결과 참조. UI 클릭 동작의 PC 확인은 별도 기록이 필요합니다.

## 6. GitHub Actions에서 **실제로 실행된 두 폴더 Git 로그**

[Reproduce two-clone Git practice — 성공 실행 #37734786124](https://github.com/Huihuing/reimagined-broccoli/actions/runs/37734786124)

GitHub Actions Ubuntu 러너 **한 대**에서 동일 저장소를 `git-practice-minsu`와 `git-practice-jiyun`로 실제 clone하고, 원격 PR 작업 당시의 공통 부모 `81f30c7`로 **임시 main을 되돌려** 과거 Git merge/pull을 재현했습니다. 이 되돌림은 CI 임시 폴더 안에서만 실행했으며 GitHub 원격 `main`이나 사용자 PC 파일은 수정하지 않았습니다.

실제 CI 로그에서 발췌 (명령과 결과):

```text
$ git clone <same origin> git-practice-minsu
Cloning into 'git-practice-minsu'...
$ git clone <same origin> git-practice-jiyun
Cloning into 'git-practice-jiyun'...

========== minsu clone ==========
origin https://github.com/Huihuing/reimagined-broccoli.git (fetch)
origin https://github.com/Huihuing/reimagined-broccoli.git (push)
$ git switch -c feature/minsu origin/feature/minsu
Switched to a new branch 'feature/minsu'
$ git switch main
Your branch is behind 'origin/main' by 7 commits, and can be fast-forwarded.
$ git merge feature/minsu (main receives changes)
Updating 81f30c7..1b3b4a1
Fast-forward
$ git pull --ff-only origin main
Updating 1b3b4a1..f4273d9
Fast-forward
$ git branch -d feature/minsu
Deleted branch feature/minsu (was 1b3b4a1).
minsu PASS: two role files + checklist exist after pull

========== jiyun clone ==========
origin https://github.com/Huihuing/reimagined-broccoli.git (fetch)
origin https://github.com/Huihuing/reimagined-broccoli.git (push)
$ git switch -c feature/jiyun origin/feature/jiyun
Switched to a new branch 'feature/jiyun'
$ git switch main
Your branch is behind 'origin/main' by 7 commits, and can be fast-forwarded.
$ git merge feature/jiyun (main receives changes)
Updating 81f30c7..64baa4a
Fast-forward
$ git pull --ff-only origin main
Updating 64baa4a..f4273d9
Fast-forward
$ git branch -d feature/jiyun
Deleted branch feature/jiyun (was 64baa4a).
jiyun PASS: two role files + checklist exist after pull
```

**증빙의 범위:** 위 clone/merge/pull은 원본 GitHub Actions 로그에 실제 존재합니다. 사용자 개인 Windows PC에서 수행한 명령 출력은 여전히 별도로 필요합니다. 이 문서의 'PC 작업 미수집' 표시는 **사용자 PC만** 가리킵니다.

## 7. Next.js 앱 변경의 GitHub Flow — 선택 심화 #2

- 최신 `main`에서 새 작업 브랜치 `feature/next-notes-app` 생성
- 실제 변경 파일: `next-practice/app/`, `next-practice/components/`, `next-practice/package.json`, `next-practice/package-lock.json`, Playwright 테스트, README, CI 워크플로, 제출 기록
- PR: [#4 — Next.js 메모 앱](https://github.com/Huihuing/reimagined-broccoli/pull/4), `base=main`, `head=feature/next-notes-app`
- 작업·검토: `Files changed` 확인, [Next.js 테스트 자동 검증](https://github.com/Huihuing/reimagined-broccoli/actions/runs/37735060792)
- 자동 검증의 실제 출력: `npm ci`, `npm run build`, `npm run start`의 `/`·`/notes` HTTP 확인 성공; **Playwright 3 passed (2.5s)**, lockfile 동기화 커밋 `722ffd916d549232821df2f0f1bcc978cd60fa5e`
- 병합 여부: PR 원본 `Merged` 상태에서 최종 확인. 각 사용자 PC에서 `git pull`한 출력은 아직 별도 수집 필요.

Next.js 기능을 Git 브랜치→커밋→PR→자동 테스트→검토→병합으로 연결한 기록입니다.

## 8. 선택 심화 1 — **실제 같은 줄 충돌 발생 및 해결**

- 파일: `checklist.md`, **1행 제목**
- 최초 공통 기반: main `db52f2d22f62992605c3364a3abfdf9a00c96ee0`
- 민수 브랜치: `feature/conflict-minsu` → `# 민수·지윤 Git 협업 점검표 — 민수 확정안`, [PR #5](https://github.com/Huihuing/reimagined-broccoli/pull/5), 먼저 **Create a merge commit** 병합 (`a511e1f6dae28bd82f0e3ae7788cba279357a0be`)
- 지윤 브랜치: `feature/conflict-jiyun` → `# 민수·지윤 Git 협업 점검표 — 지윤 정리안`, [PR #6](https://github.com/Huihuing/reimagined-broccoli/pull/6)
- 지윤 브랜치에서 **최신 origin/main 병합** 실행: [실제 Git 충돌 로그](https://github.com/Huihuing/reimagined-broccoli/actions/runs/37736727608) — GitHub Actions 임시 clone에서 실행함
- 충돌 기록: `CONFLICT (content): Merge conflict in checklist.md`, `Automatic merge failed`, `MERGE_EXIT=1`, `git ls-files -u checklist.md`로 base/ours/theirs 3단계 인덱스 검증
- 해결 제목: **`# 민수·지윤 Git 협업 점검표 — 민수 검토 + 지윤 정리 통합안`**
- 선택 이유: 민수의 검토와 지윤의 정리 의도를 모두 명시하여 한쪽 역할의 변경을 지우지 않고 통합하려고 함
- 해결 방식: 충돌 마커 제거 → `git add checklist.md` → 동일 지윤 작업 브랜치에서 **2-parent merge commit** `f4891e014440c9b489fe7fe7ff9d2fe6ba860876` → `git push origin HEAD:feature/conflict-jiyun`. 새 PR이 아니라 기존 PR #6에 자동 반영됨.
- 이후 PR #6을 merge commit으로 main에 반영하고 두 폴더에서 pull하도록 자동 확인 워크플로 `check-conflict-pulls.yml` 추가.

실제 CI 충돌 로그 발췌:

```text
Auto-merging checklist.md
CONFLICT (content): Merge conflict in checklist.md
Automatic merge failed; fix conflicts and then commit the result.
MERGE_EXIT=1
100644 4bb1aee73f09859aeff1497b1fd838f49e1e7c38 1 checklist.md
100644 fd4bba131de2988f0f111a723f65741ef2eddc96 2 checklist.md
100644 b9dc5670c13c72f95d3530baf0cd60bf8cc5dc29 3 checklist.md
[feature/conflict-jiyun f4891e0] fix(git): resolve same-line conflict on existing jiyun PR
commit=f4891e014440c9b489fe7fe7ff9d2fe6ba860876
parents=f566100732ec42cedef69679bcf5617197b3a48d a511e1f6dae28bd82f0e3ae7788cba279357a0be
PASS: actual checklist.md conflict resolved and pushed to same PR #6
```

**PC 상태에 대한 구분:** 이 실습은 GitHub Actions의 실제 임시 작업 폴더에서 수행했다. Windows PC 자체의 pull 기록이라고 주장하지 않는다.

## 9. 심화 1 최종 병합 및 양쪽 pull 재검증 (2026-10-08)

- 민수 PR: [#5](https://github.com/Huihuing/reimagined-broccoli/pull/5), **Merged**, merge commit `a511e1f6dae28bd82f0e3ae7788cba279357a0be`
- 지윤 PR: [#6](https://github.com/Huihuing/reimagined-broccoli/pull/6), 같은 줄 충돌 해결 커밋 `f4891e0`을 **기존 PR에 추가한 다음** **Merged**, merge commit `384a133479e449472033e9d18f0b4df6ec7cf4c5`
- 충돌 실행 로그: [Resolve same-line checklist conflict #37736727608](https://github.com/Huihuing/reimagined-broccoli/actions/runs/37736727608), `CONFLICT (content): Merge conflict in checklist.md`와 해결 2-parent 커밋 확인
- 양쪽 pull 실행 로그: [Verify post-conflict pulls in both clones #37736836073](https://github.com/Huihuing/reimagined-broccoli/actions/runs/37736836073), GitHub Actions 러너의 **서로 다른 두 임시 clone 폴더**에서 `git switch main` → `git pull --ff-only origin main`을 실제 실행, 결과 두 폴더 **PASS**

```text
=== minsu latest main pull after PR #6 ===
Updating a511e1f..384a133
Fast-forward
# 민수·지윤 Git 협업 점검표 — 민수 검토 + 지윤 정리 통합안
PASS minsu: origin main pull includes final conflict resolution
=== jiyun latest main pull after PR #6 ===
Updating a511e1f..384a133
Fast-forward
# 민수·지윤 Git 협업 점검표 — 민수 검토 + 지윤 정리 통합안
PASS jiyun: origin main pull includes final conflict resolution
```

CI 임시 두 clone에서 실행한 실제 로그이며 사용자 Windows PC에서 직접 조작했다고 기재하지 않습니다.

## 10. 선택 심화 3·4: Next.js ↔ Flask ↔ PostgreSQL 영구 메모 CRUD

- 구현 PR: [#7 — Next.js Flask/PostgreSQL API 통합](https://github.com/Huihuing/reimagined-broccoli/pull/7), **Merged**, merge commit `3be0b34181f8bcf1365553da35dbabaf5cd062cb`
- 작업 브랜치: `feature/next-flask-crud`, base `main`
- 실제 추가 코드: [monitor/next-frontend/](monitor/next-frontend/) `app/page.js`, `app/layout.js`, `components/DatabaseNotes.jsx`, `lib/api.js`, `next.config.mjs`, `package.json`, `package-lock.json`, `playwright.config.cjs`, `tests/db-notes.spec.cjs`, `README.md`, `.env.example`
- 기존 DB 준비 SQL: [monitor/backend/sql/001_monitor.sql](monitor/backend/sql/001_monitor.sql), `observation_notes` 테이블, 기존 Flask 경로 [monitor/backend/routes/notes.py](monitor/backend/routes/notes.py)
- 데이터 경로: Next 화면 `/api/*` fetch → `next.config.mjs` rewrite → 기존 Flask `localhost:5200/api/*` → psycopg 매개변수 쿼리 → PostgreSQL
- 인증 경로: 기존 `/api/auth/login`, `/api/auth/session`, `/api/auth/logout` 사용, 로그인 없는 메모 API는 **401**
- GET `/api/notes`, GET `/api/notes/:id`, POST `/api/notes` (201), PUT `/api/notes/:id` (200), DELETE `/api/notes/:id` (200) 실질 데이터 조회·등록·수정·삭제
- 취소: 수정 취소에 PUT 없음, 삭제 취소에 DELETE 없음. 변경 없이 DB 보존 확인
- 빈 제목/내용: 폼 오류 + 직접 Flask PUT 빈 본문 400, 기존 본문 보존 확인
- 없는 메모: GET/PUT/DELETE 404, UI에서 실패 메시지로 표시하고 성공 메시지를 표시하지 않음
- DB 지속성: 등록 후 브라우저 리로드, 수정 후 리로드, 삭제 후 리로드 각각 PostgreSQL 값 검증
- 성공 후 목록과 상세를 다시 조회하여 화면과 DB 일치를 확인
- 자동 검증 원본: [Next Flask PostgreSQL CRUD #37737427371](https://github.com/Huihuing/reimagined-broccoli/actions/runs/37737427371) — PostgreSQL16 실행, 원본 SQL 적용, Flask 로그인 계정·API 실제 실행, `npm ci`, `npm run build`, Next 프로덕션 서버와 Chromium E2E **2 passed (5.0s)**, lockfile 자동 생성·커밋
- 별도 재검증: [#37737433543](https://github.com/Huihuing/reimagined-broccoli/actions/runs/37737433543) — **2 passed (4.8s)**
- 실행 순서와 실제 설정 위치: [monitor/next-frontend/README.md](monitor/next-frontend/README.md)
- 환경 예시: `monitor/backend/.env.example`, `monitor/next-frontend/.env.example`. 실제 `.env`, DB 암호, 세션 비밀키는 Git에서 제외.

**과제 간 차이:** 필수 `next-practice/` 메모는 state 기반으로 새로고침에 초기화되는 게 정상이고, 이 심화 `monitor/next-frontend/` 메모는 PostgreSQL 저장으로 새로고침 후에도 남습니다.
