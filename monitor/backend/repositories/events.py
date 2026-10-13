from db import connect_db


def classify_event(path: str, status: int) -> str:
    if path in ("/api/auth/login", "/login", "/auth/login"):
        if status == 401:
            return "login_failure"
        if status == 200:
            return "login_success"
    return "http_request"


def create_event(payload: dict) -> dict:
    event_type = classify_event(payload["path"], payload["status"])
    with connect_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO request_events (service, method, path, status, duration_ms, occurred_at, event_type)
            VALUES (%s, %s, %s, %s, %s, COALESCE(%s::timestamptz, NOW()), %s)
            RETURNING id, service, method, path, status, duration_ms, occurred_at, event_type
            """,
            (payload.get("service", "general"), payload["method"], payload["path"],
             payload["status"], payload.get("duration_ms"), payload.get("timestamp"), event_type),
        )
        event = cursor.fetchone()
        conn.commit()
        return event


def list_events(path_query: str = "", status_code: int | None = None, event_type: str = "") -> list[dict]:
    clauses: list[str] = []
    params: list[object] = []
    if path_query:
        clauses.append("path ILIKE %s")
        params.append(f"%{path_query}%")
    if status_code is not None:
        clauses.append("status = %s")
        params.append(status_code)
    if event_type:
        clauses.append("event_type = %s")
        params.append(event_type)
    where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    with connect_db() as conn:
        cursor = conn.execute(
            f"""SELECT id, service, method, path, status, duration_ms, occurred_at, event_type
                FROM request_events {where_sql} ORDER BY id DESC""",
            tuple(params),
        )
        return cursor.fetchall()
