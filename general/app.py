from flask import Flask

from request_logging import register_request_logging
from routes.posts import posts_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "mini-watch-board"
    app.register_blueprint(posts_bp)
    register_request_logging(app)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5100, debug=True)
