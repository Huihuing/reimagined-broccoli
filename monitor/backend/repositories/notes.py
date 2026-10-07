from db import connect_db


def list_notes() -> list[dict]:
    with connect_db() as conn:
        cursor = conn.execute(
            """
            SELECT id, title, body, status, created_at, updated_at
            FROM observation_notes
            ORDER BY id DESC
            """
        )
        return cursor.fetchall()


def find_note(note_id: int) -> dict | None:
    with connect_db() as conn:
        cursor = conn.execute(
            """
            SELECT id, title, body, status, created_at, updated_at
            FROM observation_notes
            WHERE id = %s
            """,
            (note_id,),
        )
        return cursor.fetchone()


def create_note(title: str, body: str, status: str) -> dict:
    with connect_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO observation_notes (title, body, status)
            VALUES (%s, %s, %s)
            RETURNING id, title, body, status, created_at, updated_at
            """,
            (title, body, status),
        )
        note = cursor.fetchone()
        conn.commit()
        return note


def update_note(
    note_id: int,
    title: str,
    body: str,
    status: str,
) -> dict | None:
    with connect_db() as conn:
        cursor = conn.execute(
            """
            UPDATE observation_notes
            SET
                title = %s,
                body = %s,
                status = %s,
                updated_at = NOW()
            WHERE id = %s
            RETURNING id, title, body, status, created_at, updated_at
            """,
            (title, body, status, note_id),
        )
        note = cursor.fetchone()
        conn.commit()
        return note


def delete_note(note_id: int) -> dict | None:
    with connect_db() as conn:
        cursor = conn.execute(
            """
            DELETE FROM observation_notes
            WHERE id = %s
            RETURNING id, title, body, status, created_at, updated_at
            """,
            (note_id,),
        )
        note = cursor.fetchone()
        conn.commit()
        return note
