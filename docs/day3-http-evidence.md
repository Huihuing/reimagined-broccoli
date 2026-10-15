# 5과목 Day3 — 실제 요청 로그로 검토 후보와 근거 화면 만들기

기준: `Huihuing/reimagined-broccoli`의 기존 Day2 완료 코드. 기존 게시글·감시 계정·메모·네트워크·DB 볼륨은 그대로 둔다. 공개 `m5d3-start`는 참고만 하며 **구판 m5d3-solution 코드를 최신 정답으로 복사하지 않는다**.

## 1. 구성 및 수업 파일과 본인 파일의 대응

| 수업 개념 | 이 저장소의 코드 | 역할 |
| --- | --- | --- |
| 응답 후 기록 | `general/app.py`의 `app.after_request(record_request)`, `general/request_logging.py` | `method/path/status`로 원본 생성 후 stdout JSON 출력 **및 별도** 감시 API POST |
| 전송과 수신 | `compose-general.yaml`의 `MONITOR_URL`, 양쪽 `EVENT_TOKEN`, `monitor/backend/routes/events.py` | 헤더 토큰 검사, JSON 오류 처리. 콘솔 JSON만으로 DB 저장 성공을 보증하지 않음 |
| 분류 | `monitor/backend/event_rules.py::make_event` | GET / + 200 → `post_list`, 404 → `request_error`, 로그인 401/200은 기존 `login_failure`/`login_success` 유지 |
| DB 저장 | `monitor/backend/repositories/events.py::create_event` | 모니터 PostgreSQL의 **request_events** 테이블에 INSERT, DB의 자동 ID 및 `NOW()` 수신·저장시각 사용 |
| 실제 파일 캡처 | `monitor/backend/learning/capture_case.py` | 일반 서비스에 실제 GET / N회, GET /training-missing 1회, 캡처 직전 마지막 DB ID보다 큰 **실제 저장 행** 조회. SQL INSERT/고정 숫자 없음 |
| 정규화 | `learning/normalize.py::normalize_event` | 원본 딕셔너리 복사, `http-<원본숫자ID>`, `source=http_live`, `kind=event_type`, 방법·경로·상태·DB 수신시각 보존. 사용자/IP 만들지 않음 |
| 조회 선택 | `learning/http_rules.py::select_views` | `method == GET`, `path == /`, `status_code == 200`, `kind == post_list` **모두 참인 실제 행만 선택** |
| 판정/문맥 | `learning/http_rules.py::evaluate`, `find_following_errors` | `len(views) >= threshold`; 마지막 조회 DB 수신시각 뒤 `0 < seconds <= 30`의 404를 **조회 개수가 아닌 근거에만** 추가 |
| 시간·ID 범위 | `learning/support.py` | 새 관찰 시작의 `MAX(id)` 이후, **첫 분석 결과의 기준시각**을 기준으로 최근 60초, DB의 `occurred_at` 사용 |
| 보고서 | `learning/report.py::build_report` | 한 개의 HTTP 규칙 카드: 조회 수·기준·판정·이유·view_ids·404 IDs·원본 근거 records/evidence |
| 보호된 API | `monitor/backend/routes/analysis.py` | 로그인 검사, 범위/시간/기준 입력값 검증, 시작 `GET /api/analysis/start`, 결과 `GET /api/analysis` |
| 화면 | `monitor/next-frontend/components/AnalysisClient.js` | 새 관찰, 기준 입력, 결과 다시 불러오기, 6개 근거 열. Next 서버 프록시 `app/api/[...path]/route.js`를 통해 API 호출 |

**기존 저장 구조 대응**: 수업의 `http_events.id/status_code/event_type/occurred_at`에 대응하는 실제 DB는 `request_events.id/status/event_type/occurred_at`다. 별도 새 테이블을 만들거나 이름을 바꾸지 않는다. 분석 정규화 결과만 `status_code`라는 이름으로 사용한다. `request_events.occurred_at=NOW()`는 **감시 DB가 받은 시각**이며 일반 서버가 보낸 `timestamp`나 브라우저 시간을 분석에 사용하지 않는다. 근거 `http-173`은 `request_events.id=173`을 가리킨다.

## 2. 로컬 Docker 및 계정 확인 (Windows CMD)

기존 저장소 루트에서 실행한다. 계정·볼륨이 있으면 **초기화하지 말고 재사용**한다. 수업의 Day3 폴더 전체를 새로 복제하거나 덮어쓰지 않는다.

```cmd
docker network create rb-events
docker compose -f compose-monitor.yaml up -d --build
docker compose -f compose-general.yaml up -d --build
```

`docker network create`가 이미 존재한다고 하면 기존 공유망을 사용한다. 일반 `http://localhost:8081`, 감시 `http://localhost:8082`. 이전 버전 실행 중이라면 코드와 새 Python 패키지를 반영하려고 처음에 **`up -d --build monitor-api`**를 실행한다. 웹 UI 변경은 `up -d --build monitor-web`로 반영하며 게이트웨이 필요 시 restart한다.

```cmd
docker compose -f compose-monitor.yaml up -d --build monitor-api
docker compose -f compose-monitor.yaml up -d --build monitor-web
docker compose -f compose-monitor.yaml restart monitor-gateway
```

감시 계정이 없다면 기존 `monitor/backend/create_user.py`를 해당 감시 DB에서 실행해야 한다(예: `docker compose -f compose-monitor.yaml exec monitor-api python create_user.py --username operator --name "운영자"`). 임의의 비밀번호를 사용하고 로그에 적지 않는다. 실제 .env와 운영 비밀값은 Git에 넣지 않는다.

로컬 Compose: 일반 `MONITOR_URL=http://monitor-api:5000/api/events`, 서버 두 곳의 동일한 **로컬 전용** `EVENT_TOKEN`, 모니터 `GENERAL_URL=http://general-api:5000`. 모니터의 `./monitor/backend/learning:/app/learning:ro` 마운트는 호스트 생성 observation 파일을 읽기 위한 것이다. Render 클라우드는 실습 캡처 대상이 아니다.

## 3. 같은 observation.json을 사용하는 파일 실습

저장소 루트 **Windows CMD**에서 실행한다. 터미널 명령의 `>`는 호스트 임시 파일에 **실제** JSON을 기록하고, `&& move /Y`는 성공한 경우에만 최종 파일로 교체한다. 명령 실패 시 다음 단계로 넘어가지 않는다.

```cmd
if not exist monitor\backend\learning\data mkdir monitor\backend\learning\data
docker compose -f compose-monitor.yaml exec -T monitor-api python -m learning.capture_case 4 > monitor\backend\learning\data\observation-next.json && move /Y monitor\backend\learning\data\observation-next.json monitor\backend\learning\data\observation.json
docker compose -f compose-monitor.yaml exec -T monitor-api python -m learning.lesson2
docker compose -f compose-monitor.yaml exec -T monitor-api python -m learning.lesson3
docker compose -f compose-monitor.yaml exec -T monitor-api python -m learning.lesson4
docker compose -f compose-monitor.yaml exec -T monitor-api python -m learning.lesson5
```

`lesson2/3/4/5`는 **똑같은** `learning/data/observation.json`을 읽는다. 4회 성공 사례는 실제 DB 원본 5행(조회 4, 별도 404 1), 정규화 5행, 선택 조회 4행, 기준10 미해당이 예상된다. 404 원본은 정규화 중 버리지 않는다.

## 4. 실시간 화면 12회·기준 10/20 비교

1. 모니터 화면(`http://localhost:8082`)에서 로그인한 다음 **새 관찰 시작** 버튼을 누른다. 이때 DB의 마지막 원본 ID를 경계 `after_id`로 갖는다. 이전 DB 기록 DELETE는 없다.
2. **기준 10**을 선택한 상태에서 아래 12회 실습을 실행한다. 다른 브라우저 탭에서 게시판을 갱신하지 않는다.

```cmd
docker compose -f compose-monitor.yaml exec -T monitor-api python -m learning.capture_case 12 > monitor\backend\learning\data\observation-next.json && move /Y monitor\backend\learning\data\observation-next.json monitor\backend\learning\data\observation.json
```

3. **60초 안에 첫 결과 불러오기**: 그때의 서버 시각이 `reference_time`으로 고정된다. 최근 60초와 시작 ID 이후의 행을 조회한다. 예상 관찰값 **12**, 검토 후보, 조회 근거 12행 + **뒤따른 404 1행 = 전체 13행**. `GET /training-missing`의 404는 조회 수에 더하지 않는다.
4. **새 관찰 시작을 다시 누르지 않고 기준만 20으로 바꿔 결과 불러오기**: 예상 관찰값은 **12 그대로**, 판정만 **기준 미해당**으로 바뀐다. 원본 ID 경계·reference_time·근거 ID·13행도 동일하다. 기준10으로 복구하면 다시 검토 후보다.
5. **새 관찰 시작 → 일반 요청 없음 → 결과 불러오기**: 예상 관찰값 0, 기준 미해당, 근거 0행. 이전 DB 원본은 남고 ID 경계만 달라진다.

이는 예상 시나리오일 뿐이며 **수집이 지연되거나 다른 요청이 끼거나 첫 분석까지 60초가 지나면 실제 수치는 달라질 수 있다**. 화면의 숫자는 하드코딩하지 않는다. 기준 미해당은 정상을 입증하지 않는다. 404가 시간상 뒤따랐다는 이유만으로 같은 사용자·IP·인과관계·침해를 확정할 수 없다.

## 5. 실패 진단 / 원본과 DB 재확인

```cmd
docker compose -f compose-general.yaml logs --tail 20 general-api
docker compose -f compose-monitor.yaml logs --tail 20 monitor-api
docker compose -f compose-monitor.yaml exec monitor-db psql -U postgres -d monitor_db -c "SELECT id, occurred_at, method, path, status, event_type FROM request_events ORDER BY id DESC LIMIT 15;"
```

일반 표준 출력 JSON → 감시 HTTP POST → 토큰 검사 → `request_events` DB 저장 → 정규화/선택/보고서 → Next 카드는 각각 별도 단계다. 출력 JSON만 있고 DB 원본이 없으면 `MONITOR_URL/EVENT_TOKEN`, 공유망, Flask 전송 경고를 확인한다. 60초가 지나거나 기록 지연이 있으면 새 관찰 시작부터 다시 하며, 0/13에 맞추려 DB를 지우거나 파일을 수정하지 않는다.

제출에서 `.env`, 개인 키·비밀번호·토큰, 생성된 `observation.json`, 원본 DB 덤프, node_modules, .next, 캐시 파일은 제외한다. 제출 필수는 적용된 코드·구성·README이며 실행하지 않은 테스트는 완료로 쓰지 않는다.

## 6. 선택 심화 (독립 교육용 자료)

- **경계 10회**: 새 관찰 시작 → `python -m learning.capture_case 10` → 첫 결과 기준10이면 **10 >= 10**이므로 검토 후보, 조회 10 + 뒤따른 404 1 = **11근거 행**. 확인 후 새 관찰 시작 → 12회로 기본 사례 복구. `tests/test_day3.py`는 순수 로직 검증이며 실제 캡처를 대체하지 않는다.
- **AI 후보 비교**: (a) `count = len(normalized_rows)`는 404까지 더하므로 **거절**, `select_views`의 네 조건을 쓰도록 수정. (b) `error_time - first_view_time <= 30`는 마지막 조회 기준이 아니어서 **수정**, `find_following_errors`는 **마지막 조회** 뒤 `0 < gap <= 30`를 사용. (c) `count > threshold`는 경계 10을 놓치므로 **거절**, `>=` **채택**. (d) 근거 ID를 다른 조회로 뽑으면 관찰 수와 일치하지 않으므로 **거절**. 현재 `report.build_report`가 `views`에서 카운트와 `view_ids`를 함께 만들고 같은 원본의 404만 문맥에 더하는 방법을 **채택**했다. 이는 후보 검토이며 실제 AI 모델 호출이나 로그 전송은 하지 않는다.
- **PCAP**: `python -m learning.pcap_demo`는 오프라인 교육용으로 만든 가상 패킷 파일을 쓰고 읽어 5초/1초 창별 패킷 수·바이트 합을 비교한다. 실제 게시판의 PCAP가 아니며 최종 HTTP 규칙 카드의 근거에 사용하지 않는다. 예시: 최초5초 6건/434바이트, 최초1초 2건/134바이트(패킷 시간 범위의 차이).
- **IOC**: `python -m learning.ioc_demo`는 문서 전용 IP `192.0.2.10` 지표와 같은 문자열은 일치, `198.51.100.8`은 불일치라고 비교한다. 실제 HTTP 원본에는 클라이언트 IP가 없으며 그 요청을 특정 사용자와 연결할 수 없다.

## 7. 예상과 검증 상태

| 사례 | 기대 관찰 | 별도 근거 | 확인 방식 |
| --- | --- | --- | --- |
| 실제 GET / 4회 + 없는 경로1회 | 조회4/기준10 미해당 | 원본5행, 선택4행 | capture_case+lesson2/3 |
| 실제 GET / 12회 + 없는 경로1회 | 12 >= 10, 검토 후보 | 조회12 + 4041 = 13행 | API+브라우저 근거 표 |
| 같은 자료, threshold만20 | 12 < 20, 기준 미해당 | **동일** ID·기준시각·13행 | 기준값만 변경하고 API 재조회 |
| 실제 GET / 10회 + 없는 경로1회 | 10 >= 10, 검토 후보 | 11행 | 선택 심화 경계 |
| 새 시작 뒤 추가 일반 요청 없음 | 조회0, 기준 미해당 | 0행 | 새로운 ID 경계 |

GitHub CI `.github/workflows/day3-http-evidence.yml`은 **실제** Flask HTTP 요청→PostgreSQL 행→분석 API를 실행하도록 작성했다. `tests/test_day3.py`의 합성 원본은 *순수 함수 단위 테스트 전용*이며 학생의 실제 요청 로그 근거로 쓰지 않는다. CI 최종 통과 여부는 Actions 실행 결과로 검증해야 한다.
