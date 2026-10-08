# Little Notes — Next.js 메모 앱

> 제출 저장소: https://github.com/Huihuing/reimagined-broccoli  
> 실행 위치: `next-practice/` — 기존 Flask/React 프로젝트와 독립적인 JavaScript App Router 앱

## 설치와 실행

Node.js 20.9 이상이 필요합니다 (권장: Node.js 22 LTS).

```bash
cd next-practice
npm ci
npm run dev
```

브라우저에서 `http://localhost:3000`에 접속합니다. 홈 `/`과 메모 `/notes`는 `Link`로 이동합니다.

배포 방식 테스트는 개발 서버 종료 후:

```bash
npm run build
npm run start
```

## 시작 자료와 구현 내용

Next.js 공식 create-next-app의 **JavaScript + App Router** 파일 구성을 기준으로 작성한 독립 앱입니다. 이 저장소의 기존 시작 자료는 `general/` Flask 게시판, `monitor/backend/` Flask·PostgreSQL 메모 API, `monitor/frontend/` Vite·React 대시보드입니다. 기존 코드를 변경하지 않고 이번 필수 학습용 앱을 `next-practice/`에 신규 작성했습니다.

참고: https://nextjs.org/docs/app/getting-started/installation

- `app/layout.js`: 공통 HTML 본문, 로고, 홈·메모 `Link`, footer, 메타데이터
- `app/page.js`: 홈 화면, Counter 조립
- `app/notes/page.js`: 메모 화면, Notes 조립
- `components/Counter.js`: `"use client"` + `useState`로 숫자 증가/초기화
- `components/Notes.js`: `"use client"` + `useState`로 입력, ID 기반 메모 등록·수정·삭제 및 삭제 확인
- `app/globals.css`: 모바일/데스크톱 반응형 스타일

### Next.js와 React 관계

**React**는 상태(`useState`)와 컴포넌트로 인터페이스를 만드는 라이브러리이고 **Next.js**는 React 위에 파일 기반 라우팅, 서버 렌더링, 빌드·실행 구조를 제공하는 프레임워크입니다.

`page.js`는 한 주소의 화면을 정의하고 `layout.js`는 해당 경로 아래에서 공통으로 사용할 HTML 구조와 내비게이션을 정의합니다. App Router에서 기본 페이지와 레이아웃은 Server Component입니다.

버튼 클릭, 입력 변경, 메모 상태 갱신에는 브라우저 이벤트 및 React state가 필요하므로 **Counter.js와 Notes.js에 `"use client"`**를 선언했습니다. 루트 레이아웃 전체를 Client Component로 만들 필요가 없습니다.

### 메모 저장 방식

- 초기 메모는 ID 1, 2로 구별됩니다.
- 신규 ID는 `useRef` 카운터로 증가하고, 목록은 `map()`과 `key={note.id}`로 표시합니다.
- 수정 시 선택한 ID의 현재 내용을 입력칸에 채워주고, 저장하면 그 ID 하나만 바뀝니다. 취소는 원래 데이터를 건드리지 않습니다.
- 삭제 버튼 → 확인 모달 → 취소 또는 확정 순서이며 삭제 중이던 메모를 수정하고 있었다면 폼을 초기화합니다.
- 내용이 `trim()` 후 빈 문자열이면 저장하지 않고 경고 메시지를 보여줍니다.
- 모든 메모를 삭제하면 빈 목록 안내를 표시합니다.

**새로고침하면 초기 메모로 돌아오는 것이 정상**입니다. 배열이 React 컴포넌트 메모리에만 존재하고 DB/localStorage에 저장되지 않기 때문입니다. PostgreSQL에 쓰는 기존 `monitor/backend`의 API 방식과 달리 새 요청이나 새로고침에서 자료를 복구하지 않습니다.

## 수동 기능 확인 체크리스트

- [ ] 홈에서 증가/초기화
- [ ] 홈↔메모 Link 이동
- [ ] 같은 내용으로 메모 두 개 추가 후 한 메모만 수정
- [ ] 수정 취소 시 원문 유지, 수정 저장 시 ID 일치 항목만 변경
- [ ] 수정 입력이 공백뿐이면 오류·원문 유지
- [ ] 삭제 취소 시 메모 유지, 삭제 확정 시 대상만 삭제
- [ ] 수정 중인 메모 삭제 시 입력 폼 초기화
- [ ] 모든 메모 삭제 시 빈 목록 안내
- [ ] 새로고침하면 초기 메모 2개 재등장
- [ ] `npm run build`와 `npm run start` 실행 뒤 `/`·`/notes` 확인

이 체크리스트는 **실제 브라우저에서 확인 후** 체크하세요. GitHub Actions의 빌드/HTTP 상태 결과와 사용자 PC의 클릭 테스트를 혼동하지 않습니다.

## 보안 및 제출

`.env`, 비밀번호, 토큰, `node_modules/`, `.next/`는 커밋·ZIP에 넣지 않습니다. `package.json`, npm으로 생성한 `package-lock.json`, 소스와 이 README가 제출 대상입니다.

Git 협업 증빙 및 PR 주소는 저장소 루트의 `GIT_WORK.md`에 기록합니다. 추가 심화로 기존 Flask API를 연동하려면 `monitor/backend`와 충돌하지 않도록 `monitor/next-frontend/`에 별도로 구현합니다.
