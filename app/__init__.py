from flask import Blueprint, Flask
from flask_bcrypt import Bcrypt
from flask_restful import Api

from app.config import Config
from app.db import connect_mongo
from app.resources.routes import setup_resources


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    connect_mongo(app)

    api_bp = Blueprint("api", __name__)
    api = Api(api_bp)
    setup_resources(api)

    app.register_blueprint(api_bp, url_prefix="/api")

    Bcrypt(app)

    return app
