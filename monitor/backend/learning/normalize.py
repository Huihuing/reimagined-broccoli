"""Normalize real rows without changing the input mapping or inventing identities."""
from datetime import datetime


def normalize_event(original: dict) -> dict:
    raw = dict(original)
    original_id = int(raw["id"])
    received = raw["occurred_at"]
    received_at = received.isoformat() if isinstance(received, datetime) else str(received)
    # DB currently calls the HTTP status column 'status', not 'status_code'.
    code = int(raw["status"] if "status" in raw else raw["status_code"])
    return {
        "id": f"http-{original_id}",
        "original_id": original_id,
        "source": "http_live",
        "kind": raw["event_type"],
        "method": raw["method"],
        "path": raw["path"],
        "status_code": code,
        "received_at": received_at,
        "occurred_at": received_at,
        "raw": {**raw, "occurred_at": received_at},
    }


def normalize_events(rows):
    return [normalize_event(row) for row in rows]
