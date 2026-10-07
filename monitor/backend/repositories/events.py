from db import connect_db


def create_event(payload: dict) -> dict:
    with connect_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO request_events (
                service,
                method,
                path,
                status,
                duration_ms,
                occurred_at
            )
            VALUES (%s, %s, %s, %s, %s, COALESCE(%s::timestamptz, NOW()))
            RETURNING id, service, method, path, status, duration_ms, occurred_at
            """,
            (
                payload.get("service", "general"),
                payload["method"],
                payload["path"],
                payload["status"],
                payload.get("duration_ms"),
                payload.get("timestamp"),
            ),
        )
        event = cursor.fetchone()
        conn.commit()
        return event


def list_events(
    path_query: str = "",
    status_code: int | None = None,
) -> list[dict]:
    clauses: list[str] = []
    params: list[object] = []

    if path_query:
        clauses.append("path ILIKE %s")
        params.append(f"%{path_query}%")

    if status_code is not None:
        clauses.append("status = %s")
        params.append(status_code)

    where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""

    with connect_db() as conn:
        cursor = conn.execute(
            f"""
            SELECT id, service, method, path, status, duration_ms, occurred_at
            FROM request_events
            {where_sql}
            ORDER BY id DESC
            """,
            tuple(params),
        )
        return cursor.fetchall()
