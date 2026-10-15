"""Synthetic fixtures test PURE rule logic only, never used as submitted live evidence."""
from datetime import datetime, timedelta, timezone

from learning.normalize import normalize_event, normalize_events
from learning.http_rules import select_views, find_following_errors, evaluate
from learning.report import build_report

ORIGIN = datetime(2026, 10, 15, 10, 0, tzinfo=timezone.utc)


def row(id, method="GET", path="/", status=200, kind="post_list", seconds=0):
    return {
        "id": id, "service": "general", "method": method,
        "path": path, "status": status, "event_type": kind,
        "occurred_at": ORIGIN + timedelta(seconds=seconds),
    }


def test_normalization_preserves_raw_id_time_and_kind():
    source = row(42, seconds=7)
    clone = dict(source)
    normalized = normalize_event(source)
    assert source == clone
    assert normalized["id"] == "http-42"
    assert normalized["original_id"] == 42
    assert normalized["source"] == "http_live"
    assert normalized["kind"] == "post_list"
    assert normalized["status_code"] == 200
    assert normalized["received_at"] == source["occurred_at"].isoformat()
    assert "user" not in normalized and "ip" not in normalized


def test_four_conditions_and_following_error_window():
    orig = [
        row(1, seconds=0), row(2, "POST", "/", 200, "post_list", 1),
        row(3, "GET", "/board", 200, "post_list", 2),
        row(4, "GET", "/", 404, "request_error", 3),
        row(5, "GET", "/", 200, "http_request", 4),
        row(6, seconds=5),
        row(7, "GET", "/training-missing", 404, "request_error", 35),
        row(8, "GET", "/too-late", 404, "request_error", 36),
        row(9, "GET", "/too-early", 404, "request_error", 5),
    ]
    norm = normalize_events(orig)
    views = select_views(norm)
    assert [e["id"] for e in views] == ["http-1", "http-6"]
    assert [e["id"] for e in find_following_errors(norm, views)] == ["http-7"]
    assert find_following_errors(norm, []) == []
    assert not evaluate(views, 10)


def test_one_card_12_views_plus_one_404_same_evidence_threshold_10_20():
    source = [row(i, seconds=i / 100) for i in range(1, 13)]
    source.append(row(13, "GET", "/training-missing", 404, "request_error", .25))
    result10 = build_report(source, 10, 0, ORIGIN)
    result20 = build_report(source, 20, 0, ORIGIN)
    a, b = result10["card"], result20["card"]
    assert (a["observed"], a["verdict"], len(a["evidence"])) == (12, "검토 후보", 13)
    assert (b["observed"], b["verdict"], len(b["evidence"])) == (12, "기준 미해당", 13)
    assert a["view_ids"] == b["view_ids"]
    assert a["evidence"] == b["evidence"]
    assert a["following_error_ids"] == ["http-13"]
    assert "http-13" not in a["view_ids"]


def test_threshold_equality_and_empty_observation():
    source = [row(i, seconds=i / 10) for i in range(1, 11)]
    source.append(row(11, "GET", "/training-missing", 404, "request_error", 2))
    report = build_report(source, 10, 100, ORIGIN)
    assert report["card"]["observed"] == 10
    assert report["card"]["matched"]
    assert len(report["card"]["records"]) == 11
    empty = build_report([], 10, 200, ORIGIN)["card"]
    assert empty["observed"] == 0
    assert empty["following_error_count"] == 0
    assert empty["evidence"] == []
