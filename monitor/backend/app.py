import os
from pathlib import Path
from flask import Flask, abort, jsonify, session
from dotenv import load_dotenv
from routes import auth_bp, events_bp, notes_bp
from observability import configure_errors

load_dotenv(Path(__file__).with_name(".env"), interpolate=False)


def create_app() -> Flask:
    configure_errors("mini-monitor")
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY") or os.getenv("SESSION_SECRET", "dev-only-change-me"),
        SESSION_COOKIE_NAME="monitor_session",
        SESSION_COOKIE_SECURE=os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )
    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(notes_bp)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "service": "monitor"})

    @app.get("/api/sentry-test")
    def sentry_test():
        if os.getenv("ENABLE_SENTRY_TEST", "false").lower() != "true":
            abort(404)
        if not session.get("user"):
            return jsonify({"error": "로그인이 필요합니다."}), 401
        return jsonify({"result": 1, "status": "ok"})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5200, debug=False)
