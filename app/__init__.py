from logging.config import dictConfig

from flask import Blueprint, Flask
from flask_bcrypt import Bcrypt
from flask_restful import Api

from app.config import Config
from app.db import connect_mongo
from app.resources.routes import setup_resources


def create_app():
    """
    Factory function that creates and configures the Flask application.

    This function initializes a new Flask application, sets up logging, loads configuration from the
    Config object, establishes the database connection, sets up the API routes,
    and registers the necessary extensions.

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

    @app.route("/")
    def hello() -> str:
        return "Hello! This is a Users API in Flask and MongoDB"

    Bcrypt(app)

    return app
