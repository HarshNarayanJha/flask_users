from flask import Flask
from mongoengine import connect


def connect_mongo(app: Flask):
    connect(host=app.config["MONGODB_URI"])
