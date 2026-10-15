"""Authenticated analysis API: start a new ID boundary; reuse the first result time."""
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from auth_required import login_required
from learning.support import get_latest_id, read_live_events
from learning.report import build_report

analysis_bp = Blueprint("analysis", __name__)


@analysis_bp.get("/api/analysis/start")
@login_required
def start_observation():
    # Starting a new observation NEVER deletes DB records.
    return jsonify({"after_id": get_latest_id()})


@analysis_bp.get("/api/analysis")
@login_required
def analyze():
    raw_id = request.args.get("after_id")
    raw_threshold = request.args.get("threshold", "10")
    if raw_id is None or not raw_id.isdecimal() or not raw_threshold.isdecimal():
        return jsonify({"error": "after_id와 threshold는 정수여야 합니다."}), 400
    after_id, threshold = int(raw_id), int(raw_threshold)
    if not 0 <= after_id <= 9223372036854775807 or not 1 <= threshold <= 10000:
        return jsonify({"error": "관찰 경계 또는 기준 범위가 올바르지 않습니다."}), 400
    raw_reference = request.args.get("reference_time")
    reference = None
    if raw_reference:
        try:
            reference = datetime.fromisoformat(raw_reference.replace("Z", "+00:00"))
            if reference.tzinfo is None or reference > datetime.now(timezone.utc):
                raise ValueError
        except ValueError:
            return jsonify({"error": "유효한 timezone 포함 reference_time이 필요합니다."}), 400
    rows, reference = read_live_events(after_id, reference)
    return jsonify(build_report(rows, threshold, after_id, reference))


@analysis_bp.get("/api/analysis/raw")
@login_required
def original_observation():
    raw_id = request.args.get("after_id", "0")
    if not raw_id.isdecimal() or int(raw_id) > 9223372036854775807:
        return jsonify({"error": "after_id는 양의 정수 또는 0이어야 합니다."}), 400
    rows, reference = read_live_events(int(raw_id))
    # This API also uses the same ID+60s window, never an example JSON.
    return jsonify({"after_id": int(raw_id), "reference_time": reference.isoformat(), "rows": rows})
