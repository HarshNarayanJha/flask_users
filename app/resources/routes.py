from flask_restful import Api

from .user import UserApi, UsersApi


def setup_resources(api: Api):
    api.add_resource(UsersApi, "/users")
    api.add_resource(UserApi, "/users/<string:id>")
