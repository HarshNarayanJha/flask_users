from flask_restful import Api

from .user import UserApi, UsersApi


def setup_resources(api: Api):
    """
    Configure Flask-RESTful API resources.

    Registers the UserApi and UsersApi resources with their respective URL endpoints.

    Args:
        api (Api): The Flask-RESTful API instance to add resources to.
    """
    api.add_resource(UsersApi, "/users")
    api.add_resource(UserApi, "/users/<string:id>")
