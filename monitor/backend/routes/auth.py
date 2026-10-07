from flask import Blueprint, jsonify, request, session
from werkzeug.security import check_password_hash

from repositories.users import find_user


auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/api/auth/login")
def login():
    payload = request.get_json(silent=True) or {}
    username = str(payload.get("username", "")).strip()
    password = str(payload.get("password", ""))

    if not username or not password:
        return jsonify({"error": "아이디와 비밀번호를 모두 입력해 주세요."}), 400

    user = find_user(username)
    if user is None or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "아이디 또는 비밀번호가 올바르지 않습니다."}), 401

    session["user"] = {
        "id": user["id"],
        "username": user["username"],
        "name": user["display_name"],
    }
    return jsonify({"user": session["user"]})


@auth_bp.get("/api/auth/session")
def current_session():
    user = session.get("user")
    if user is None:
        return jsonify({"authenticated": False, "user": None})
    return jsonify({"authenticated": True, "user": user})


@auth_bp.post("/api/auth/logout")
def logout():
    session.clear()
    return jsonify({"ok": True})
