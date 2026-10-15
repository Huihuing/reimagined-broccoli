"""Read immutable observations from the existing PostgreSQL request_events table."""
from datetime import datetime, timedelta, timezone
from db import connect_db


def get_latest_id():
    with connect_db() as conn:
        return int(conn.execute("SELECT COALESCE(MAX(id), 0) AS id FROM request_events").fetchone()["id"])


def read_live_events(after_id: int, reference_time: datetime | None = None):
    if type(after_id) is not int or after_id < 0:
        raise ValueError("after_id must be nonnegative")
    if reference_time is None:
        reference_time = datetime.now(timezone.utc)
    if reference_time.tzinfo is None:
        raise ValueError("reference_time requires timezone")
    reference_time = reference_time.astimezone(timezone.utc)
    start_time = reference_time - timedelta(seconds=60)
    with connect_db() as conn:
        rows = conn.execute(
            """SELECT id, service, method, path, status, duration_ms,
                      occurred_at, event_type
               FROM request_events
               WHERE service = 'general' AND id > %s
                 AND occurred_at >= %s AND occurred_at <= %s
               ORDER BY id ASC""",
            (after_id, start_time, reference_time),
        ).fetchall()
    return rows, reference_time


def read_observation_file():
    import json
    from pathlib import Path
    file_path = Path(__file__).with_name("data") / "observation.json"
    data = json.loads(file_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("original_rows"), list):
        raise ValueError("Expected actual captured original_rows in observation.json")
    return data
