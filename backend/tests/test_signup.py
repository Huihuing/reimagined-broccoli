import bcrypt
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.database import Base, SessionLocal, engine
from app.main import app
from app.models.user import User


client = TestClient(app)


def setup_module() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def teardown_module() -> None:
    Base.metadata.drop_all(bind=engine)


def test_signup_saves_hashed_password() -> None:
    response = client.post(
        "/api/auth/signup",
        json={
            "username": "broccoli_user",
            "email": "user@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "broccoli_user"
    assert body["email"] == "user@example.com"
    assert "password" not in body
    assert "password_hash" not in body

    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.username == "broccoli_user"))
        assert user is not None
        assert user.password_hash != "password123"
        assert bcrypt.checkpw(
            b"password123",
            user.password_hash.encode("utf-8"),
        )


def test_duplicate_signup_is_rejected() -> None:
    response = client.post(
        "/api/auth/signup",
        json={
            "username": "broccoli_user",
            "email": "another@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 409
