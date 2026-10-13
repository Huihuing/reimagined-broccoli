from flask import Blueprint, jsonify, redirect, render_template, request, session
from werkzeug.security import check_password_hash
from db import connect_db

auth_bp = Blueprint("general_auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
@auth_bp.post("/api/auth/login")
def login():
    if request.method == "GET":
        return render_template("login.html", error=None)
    data = request.get_json(silent=True) if request.is_json else request.form
    data = data or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", ""))
    if not username or not password:
        if request.is_json:
            return jsonify({"error": "아이디와 비밀번호를 입력해 주세요."}), 400
        return render_template("login.html", error="아이디와 비밀번호를 입력해 주세요."), 400
    with connect_db() as conn:
        row = conn.execute("SELECT id, username, password_hash FROM users WHERE username=%s", (username,)).fetchone()
    if not row or not check_password_hash(row["password_hash"], password):
        if request.is_json:
            return jsonify({"error": "아이디 또는 비밀번호 오류"}), 401
        return render_template("login.html", error="아이디 또는 비밀번호 오류"), 401
    session.clear()
    session["general_user"] = {"id": row["id"], "username": row["username"]}
    if request.is_json:
        return jsonify({"user": session["general_user"]}), 200
    return redirect("/", code=303)


@auth_bp.get("/api/auth/session")
def current_session():
    user = session.get("general_user")
    return jsonify({"authenticated": bool(user), "user": user})


@auth_bp.post("/api/auth/logout")
def logout():
    session.clear()
    return jsonify({"ok": True})
