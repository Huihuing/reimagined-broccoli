"""Persistence uses the repo's existing request_events (course name: http_events)."""
from db import connect_db


def classify_event(path: str, status: int, method: str = "GET") -> str:
    from event_rules import classify_event as decide
    return decide(method, path, status)


def create_event(payload: dict) -> dict:
    # occurred_at is assigned when the MONITOR database receives/stores the row.
    # Never trust the general server's timestamp for the analysis time window.
    with connect_db() as conn:
        row = conn.execute(
            """INSERT INTO request_events
                  (service, method, path, status, duration_ms, occurred_at, event_type)
               VALUES (%s, %s, %s, %s, %s, NOW(), %s)
               RETURNING id, service, method, path, status, duration_ms,
                         occurred_at, event_type""",
            (
                payload.get("service", "general"),
                payload["method"], payload["path"], payload["status"],
                payload.get("duration_ms"), payload["event_type"],
            ),
        ).fetchone()
        conn.commit()
        return row


def list_events(path_query: str = "", status_code: int | None = None, event_type: str = "") -> list[dict]:
    clauses = []
    params = []
    if path_query:
        clauses.append("path ILIKE %s")
        params.append("%" + path_query + "%")
    if status_code is not None:
        clauses.append("status = %s")
        params.append(status_code)
    if event_type:
        clauses.append("event_type = %s")
        params.append(event_type)
    where_sql = "WHERE " + " AND ".join(clauses) if clauses else ""
    with connect_db() as conn:
        return conn.execute(
            f"""SELECT id, service, method, path, status, duration_ms,
                       occurred_at, event_type
                 FROM request_events {where_sql} ORDER BY id DESC""",
            tuple(params),
        ).fetchall()
