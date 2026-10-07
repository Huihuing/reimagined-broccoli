from werkzeug.security import generate_password_hash

from app import create_app
from db import connect_db
from repositories.users import create_or_update_user


app = create_app()
app.config.update(TESTING=True, SECRET_KEY="test-secret")


def reset_db() -> None:
    with connect_db() as conn:
        conn.execute("DELETE FROM observation_notes")
        conn.execute("DELETE FROM request_events")
        conn.execute("DELETE FROM monitor_users")
        conn.commit()

    create_or_update_user(
        "admin",
        "운영자",
        generate_password_hash("test-password"),
    )


def setup_function() -> None:
    reset_db()


def login(client):
    return client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "test-password"},
    )


def test_login_session_logout_and_protection() -> None:
    client = app.test_client()

    assert client.post(
        "/api/auth/login",
        json={"username": "", "password": ""},
    ).status_code == 400

    assert client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "wrong"},
    ).status_code == 401

    response = login(client)
    assert response.status_code == 200
    assert response.get_json()["user"]["name"] == "운영자"

    session_response = client.get("/api/auth/session")
    assert session_response.status_code == 200
    assert session_response.get_json()["authenticated"] is True

    assert client.get("/api/notes").status_code == 200

    assert client.post("/api/auth/logout").status_code == 200
    assert client.get("/api/notes").status_code == 401
    assert client.get("/api/events").status_code == 401


def test_events_are_persisted_filtered_and_summarized() -> None:
    client = app.test_client()

    assert client.post(
        "/api/events",
        json={
            "service": "general",
            "method": "GET",
            "path": "/board/1",
            "status": 200,
            "duration_ms": 5.5,
        },
    ).status_code == 201

    assert client.post(
        "/api/events",
        json={
            "service": "general",
            "method": "GET",
            "path": "/board/999",
            "status": 404,
            "duration_ms": 4.2,
        },
    ).status_code == 201

    login(client)

    response = client.get("/api/events")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["summary"] == {"total": 2, "errors": 1}

    filtered = client.get("/api/events?path=999&status=404")
    assert filtered.status_code == 200
    data = filtered.get_json()
    assert data["summary"] == {"total": 1, "errors": 1}
    assert data["events"][0]["path"] == "/board/999"

    assert client.get("/api/events?status=abc").status_code == 400


def test_notes_crud_validation_status_and_missing() -> None:
    client = app.test_client()
    login(client)

    invalid = client.post(
        "/api/notes",
        json={"title": "   ", "body": "내용"},
    )
    assert invalid.status_code == 400

    created = client.post(
        "/api/notes",
        json={
            "title": " 404 확인 ",
            "body": " 없는 게시글 요청을 확인했다. ",
            "status": "확인 전",
        },
    )
    assert created.status_code == 201
    note = created.get_json()["note"]
    note_id = note["id"]
    assert note["title"] == "404 확인"

    listing = client.get("/api/notes")
    assert listing.status_code == 200
    assert len(listing.get_json()["notes"]) == 1

    detail = client.get(f"/api/notes/{note_id}")
    assert detail.status_code == 200

    invalid_update = client.put(
        f"/api/notes/{note_id}",
        json={
            "title": "404 확인",
            "body": "   ",
            "status": "완료",
        },
    )
    assert invalid_update.status_code == 400

    preserved = client.get(f"/api/notes/{note_id}").get_json()["note"]
    assert preserved["body"] == "없는 게시글 요청을 확인했다."
    assert preserved["status"] == "확인 전"

    updated = client.put(
        f"/api/notes/{note_id}",
        json={
            "title": "404 요청 확인 완료",
            "body": "요청 경로와 상태 코드를 확인했다.",
            "status": "완료",
        },
    )
    assert updated.status_code == 200
    assert updated.get_json()["note"]["status"] == "완료"

    deleted = client.delete(f"/api/notes/{note_id}")
    assert deleted.status_code == 200

    assert client.get(f"/api/notes/{note_id}").status_code == 404
    assert client.put(
        f"/api/notes/{note_id}",
        json={"title": "x", "body": "y", "status": "확인 전"},
    ).status_code == 404
    assert client.delete(f"/api/notes/{note_id}").status_code == 404
