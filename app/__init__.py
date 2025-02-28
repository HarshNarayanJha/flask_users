from flask import Blueprint, Flask
from flask_bcrypt import Bcrypt
from flask_restful import Api

from app.config import Config
from app.db import connect_mongo
from app.resources.routes import setup_resources


def create_app():
    """
    Factory function that creates and configures the Flask application.

    This function initializes a new Flask application, loads configuration from the
    Config object, establishes the database connection, sets up the API routes,
    and registers the necessary extensions.

    Returns:
        Flask: The configured Flask application instance ready to be run.
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    connect_mongo(app)

    api_bp = Blueprint("api", __name__)
    api = Api(api_bp)
    setup_resources(api)

    app.register_blueprint(api_bp, url_prefix="/api")

    Bcrypt(app)

    return app
