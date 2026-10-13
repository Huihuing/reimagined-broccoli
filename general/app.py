import os
from flask import Flask, abort, jsonify, session
from request_logging import register_request_logging
from routes.posts import posts_bp
from routes.auth import auth_bp
from observability import configure_errors


def create_app() -> Flask:
    configure_errors("mini-general")
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY", "local-general-dev-only-key"),
        SESSION_COOKIE_NAME="general_session",
        SESSION_COOKIE_SECURE=os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )
    app.register_blueprint(posts_bp)
    app.register_blueprint(auth_bp)
    register_request_logging(app)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "service": "general"})

    @app.get("/api/sentry-test")
    def sentry_test():
        if os.getenv("ENABLE_SENTRY_TEST", "false").lower() != "true":
            abort(404)
        if not session.get("general_user"):
            return jsonify({"error": "로그인이 필요합니다."}), 401
        # Day2 error fix: replaced the original demonstration ZeroDivisionError (1 / 0).
        return jsonify({"result": 1, "status": "ok"})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5100, debug=False)
