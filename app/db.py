from flask import Flask
from mongoengine import connect


def connect_mongo(app: Flask):
    """
    Establishes a connection to MongoDB using the URI from the Flask app config.

    Args:
        app (Flask): The Flask application instance containing the MongoDB URI
                    in its configuration as 'MONGODB_URI'.
    """
    connect(host=app.config["MONGODB_URI"])
