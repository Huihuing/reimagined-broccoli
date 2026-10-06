from urllib.parse import urlparse

from app import create_app
from db import connect_db


app = create_app()
app.config.update(TESTING=True)
client = app.test_client()


def clear_posts() -> None:
    with connect_db() as conn:
        conn.execute("DELETE FROM posts")
        conn.commit()


def get_post_count() -> int:
    with connect_db() as conn:
        row = conn.execute("SELECT COUNT(*) AS count FROM posts").fetchone()
        return row["count"]


def get_post(post_id: int):
    with connect_db() as conn:
        return conn.execute(
            "SELECT id, title, body FROM posts WHERE id = %s",
            (post_id,),
        ).fetchone()


def setup_function() -> None:
    clear_posts()


def test_empty_list_and_new_form() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "등록된 게시글이 없습니다.".encode() in response.data

    response = client.get("/board/new")
    assert response.status_code == 200
    assert b"<form" in response.data
    assert b"<input" in response.data
    assert b"<textarea" in response.data
    assert b"<button" in response.data


def test_create_detail_and_refresh_without_duplicate() -> None:
    response = client.post(
        "/board/new",
        data={"title": " 첫 글 ", "body": " 첫 내용 "},
        follow_redirects=False,
    )
    assert response.status_code == 303

    location = response.headers["Location"]
    post_id = int(urlparse(location).path.rsplit("/", 1)[-1])
    assert get_post_count() == 1

    detail = client.get(location)
    assert detail.status_code == 200
    assert "첫 글".encode() in detail.data
    assert "첫 내용".encode() in detail.data

    refreshed = client.get(location)
    assert refreshed.status_code == 200
    assert get_post_count() == 1

    listing = client.get("/")
    assert listing.status_code == 200
    assert "첫 글".encode() in listing.data
    assert f"/board/{post_id}".encode() in listing.data


def test_create_rejects_blank_input_without_insert() -> None:
    response = client.post(
        "/board/new",
        data={"title": "   ", "body": "내용"},
    )
    assert response.status_code == 400
    assert "제목을 입력해 주세요.".encode() in response.data
    assert get_post_count() == 0

    response = client.post(
        "/board/new",
        data={"title": "제목", "body": "   "},
    )
    assert response.status_code == 400
    assert "내용을 입력해 주세요.".encode() in response.data
    assert get_post_count() == 0


def test_edit_prefills_updates_and_preserves_on_invalid_input() -> None:
    created = client.post(
        "/board/new",
        data={"title": "원래 제목", "body": "원래 내용"},
        follow_redirects=False,
    )
    post_id = int(urlparse(created.headers["Location"]).path.rsplit("/", 1)[-1])

    edit_form = client.get(f"/board/{post_id}/edit")
    assert edit_form.status_code == 200
    assert "원래 제목".encode() in edit_form.data
    assert "원래 내용".encode() in edit_form.data

    invalid = client.post(
        f"/board/{post_id}/edit",
        data={"title": "   ", "body": "바뀌면 안 됨"},
    )
    assert invalid.status_code == 400
    post = get_post(post_id)
    assert post["title"] == "원래 제목"
    assert post["body"] == "원래 내용"

    updated = client.post(
        f"/board/{post_id}/edit",
        data={"title": " 수정 제목 ", "body": " 수정 내용 "},
        follow_redirects=False,
    )
    assert updated.status_code == 303
    assert urlparse(updated.headers["Location"]).path == f"/board/{post_id}"

    post = get_post(post_id)
    assert post["title"] == "수정 제목"
    assert post["body"] == "수정 내용"


def test_delete_get_does_not_delete_cancel_link_exists_and_post_deletes() -> None:
    created = client.post(
        "/board/new",
        data={"title": "삭제 대상", "body": "삭제 내용"},
        follow_redirects=False,
    )
    post_id = int(urlparse(created.headers["Location"]).path.rsplit("/", 1)[-1])

    confirm = client.get(f"/board/{post_id}/delete")
    assert confirm.status_code == 200
    assert "삭제 대상".encode() in confirm.data
    assert f"/board/{post_id}".encode() in confirm.data
    assert get_post(post_id) is not None

    deleted = client.post(
        f"/board/{post_id}/delete",
        follow_redirects=False,
    )
    assert deleted.status_code == 303
    assert urlparse(deleted.headers["Location"]).path == "/"
    assert get_post(post_id) is None

    assert client.get(f"/board/{post_id}").status_code == 404
    assert client.get(f"/board/{post_id}/edit").status_code == 404
    assert client.get(f"/board/{post_id}/delete").status_code == 404


def test_missing_post_returns_error_template_404() -> None:
    response = client.get("/board/999999")
    assert response.status_code == 404
    assert "게시글을 찾을 수 없습니다.".encode() in response.data
