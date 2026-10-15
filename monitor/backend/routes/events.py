import hmac
import os
from flask import Blueprint, jsonify, request
from auth_required import login_required
from repositories.events import create_event, list_events
from event_rules import make_event

events_bp = Blueprint("events", __name__)


@events_bp.post("/api/events")
def receive_event():
    token = os.getenv("EVENT_TOKEN", "")
    if not token:
        return jsonify({"error": "EVENT_TOKEN 서버 설정이 필요합니다."}), 503
    received = request.headers.get("X-Event-Token", "")
    if not hmac.compare_digest(received.encode(), token.encode()):
        return jsonify({"error": "기록 전송 권한이 없습니다."}), 401

    # Validation and classification are isolated in event_rules.make_event.
    event = make_event(request.get_json(silent=True))
    if event is None:
        return jsonify({"error": "method, path, status 값을 확인해 주세요."}), 400
    stored = create_event(event)
    return jsonify({"event": stored}), 201


@events_bp.get("/api/events")
@login_required
def get_events():
    path_query = request.args.get("path", "").strip()
    raw_status = request.args.get("status", "").strip()
    event_type = request.args.get("event_type", "").strip()
    if event_type and event_type not in {"login_success", "login_failure", "http_request", "post_list", "request_error"}:
        return jsonify({"error": "지원하지 않는 이벤트 유형입니다."}), 400
    status_code = None
    if raw_status:
        try:
            status_code = int(raw_status)
        except ValueError:
            return jsonify({"error": "상태 코드는 숫자로 입력해 주세요."}), 400
        if not 100 <= status_code <= 599:
            return jsonify({"error": "상태 코드는 100~599 사이여야 합니다."}), 400
    events = list_events(path_query=path_query, status_code=status_code, event_type=event_type)
    return jsonify({
        "events": events,
        "summary": {"total": len(events), "errors": sum(1 for event in events if event["status"] >= 400)},
        "filters": {"path": path_query, "status": status_code, "event_type": event_type},
    })
