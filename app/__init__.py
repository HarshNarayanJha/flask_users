from logging.config import dictConfig

from flask import Blueprint, Flask
from flask_restful import Api

from app.config import Config
from app.db import connect_mongo
from app.extensions import bcrypt, limiter
from app.resources.routes import setup_resources


def create_app():
    """
    Factory function that creates and configures the Flask application.

    Returns:
        Flask: The configured Flask application instance ready to be run.
    """

    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                }
            },
            "handlers": {"wsgi": {"class": "logging.StreamHandler", "stream": "ext://flask.logging.wsgi_errors_stream", "formatter": "default"}},
            "root": {"level": "INFO", "handlers": ["wsgi"]},
        }
    )

    app = Flask(__name__)
    app.config.from_object(Config)
    connect_mongo(app)

    api_bp = Blueprint("api", __name__)
    api = Api(api_bp)
    setup_resources(api)

    app.register_blueprint(api_bp, url_prefix="/api/v1")

    limiter.init_app(app)
    bcrypt.init_app(app)

    @app.route("/")
    def hello() -> str:
        return "Hello! This is a Users API in Flask and MongoDB"

    return app
