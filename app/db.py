from flask import Flask
from mongoengine import connect


def connect_mongo(app: Flask):
    """
    Establishes a connection to MongoDB using the URI from the Flask app config.

    Args:
        app (Flask): The Flask application instance containing the MongoDB URI
                    in its configuration as `MONGODB_URI` and dbname as `MONGODB_DBNAME`.
    """
    app.logger.info(f"connecting to mongodb: {app.config['MONGODB_URI']}, db: {app.config['MONGODB_DBNAME']}")
    connect(host=app.config["MONGODB_URI"], db=app.config["MONGODB_DBNAME"])
