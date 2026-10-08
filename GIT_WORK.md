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
