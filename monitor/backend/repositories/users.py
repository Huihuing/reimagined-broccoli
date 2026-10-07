from db import connect_db


def find_user(username: str) -> dict | None:
    with connect_db() as conn:
        cursor = conn.execute(
            """
            SELECT id, username, display_name, password_hash
            FROM monitor_users
            WHERE username = %s
            """,
            (username,),
        )
        return cursor.fetchone()


def create_or_update_user(
    username: str,
    display_name: str,
    password_hash: str,
) -> dict:
    with connect_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO monitor_users (username, display_name, password_hash)
            VALUES (%s, %s, %s)
            ON CONFLICT (username)
            DO UPDATE SET
                display_name = EXCLUDED.display_name,
                password_hash = EXCLUDED.password_hash
            RETURNING id, username, display_name
            """,
            (username, display_name, password_hash),
        )
        user = cursor.fetchone()
        conn.commit()
        return user
