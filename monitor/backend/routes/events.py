from flask import Blueprint, jsonify, request

from auth_required import login_required
from repositories.events import create_event, list_events


events_bp = Blueprint("events", __name__)


@events_bp.post("/api/events")
def receive_event():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "JSON 요청이 필요합니다."}), 400

    method = str(payload.get("method", "")).strip().upper()
    path = str(payload.get("path", "")).strip()

    try:
        status = int(payload.get("status"))
    except (TypeError, ValueError):
        status = 0

    if not method or not path or status < 100 or status > 599:
        return jsonify({"error": "method, path, status 값을 확인해 주세요."}), 400

    normalized = {
        **payload,
        "method": method,
        "path": path,
        "status": status,
    }
    event = create_event(normalized)
    return jsonify({"event": event}), 201


@events_bp.get("/api/events")
@login_required
def get_events():
    path_query = request.args.get("path", "").strip()
    raw_status = request.args.get("status", "").strip()

    status_code = None
    if raw_status:
        try:
            status_code = int(raw_status)
        except ValueError:
            return jsonify({"error": "상태 코드는 숫자로 입력해 주세요."}), 400

        if status_code < 100 or status_code > 599:
            return jsonify({"error": "상태 코드는 100~599 사이여야 합니다."}), 400

    events = list_events(path_query=path_query, status_code=status_code)
    error_count = sum(1 for event in events if event["status"] >= 400)

    return jsonify(
        {
            "events": events,
            "summary": {
                "total": len(events),
                "errors": error_count,
            },
            "filters": {
                "path": path_query,
                "status": status_code,
            },
        }
    )
