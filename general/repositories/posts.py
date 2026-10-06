from db import connect_db


def list_posts() -> list[dict]:
    with connect_db() as conn:
        cursor = conn.execute(
            "SELECT id, title, body FROM posts ORDER BY id ASC"
        )
        return cursor.fetchall()


def find_post(post_id: int) -> dict | None:
    with connect_db() as conn:
        cursor = conn.execute(
            "SELECT id, title, body FROM posts WHERE id = %s",
            (post_id,),
        )
        return cursor.fetchone()


def create_post(title: str, body: str) -> dict:
    with connect_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO posts (title, body)
            VALUES (%s, %s)
            RETURNING id, title, body
            """,
            (title, body),
        )
        post = cursor.fetchone()
        conn.commit()
        return post


def update_post(post_id: int, title: str, body: str) -> dict | None:
    with connect_db() as conn:
        cursor = conn.execute(
            """
            UPDATE posts
            SET title = %s, body = %s
            WHERE id = %s
            RETURNING id, title, body
            """,
            (title, body, post_id),
        )
        post = cursor.fetchone()
        conn.commit()
        return post


def delete_post(post_id: int) -> dict | None:
    with connect_db() as conn:
        cursor = conn.execute(
            """
            DELETE FROM posts
            WHERE id = %s
            RETURNING id, title, body
            """,
            (post_id,),
        )
        post = cursor.fetchone()
        conn.commit()
        return post
