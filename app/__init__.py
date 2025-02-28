from flask import Flask
from flask_bcrypt import Bcrypt

from app.config import Config
from app.db import connect_mongo
from app.routes import api_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    connect_mongo(app)

    app.register_blueprint(api_bp, url_prefix="/api")

    Bcrypt(app)

    return app
