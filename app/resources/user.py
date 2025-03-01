import json
from typing import Dict, Union

from flask import Response, request
from flask import current_app as app
from flask_restful import Resource
from mongoengine import DoesNotExist, NotUniqueError, ValidationError

from app.extensions import limiter
from app.models import User


class UsersApi(Resource):
    """API resource for managing multiple users."""

    decorators = [limiter.limit("30 per minute")]

    def get(self):
        """Retrieve all users from the database.

        Returns:
            List of user objects in JSON format
        """
        users = User.objects()
        user_list = [json.loads(u.to_json()) for u in users]
        return user_list, 200

    def post(self):
        """Create a new user."""

        data = request.get_json()

        required_fields = ["name", "email", "password"]
        for field in required_fields:
            if field not in data:
                return {"message": f"The '{field}' field is required"}, 400

        user = User(**data)
        try:
            user.validate()
            user.hash_password()
            user.save()
        except ValidationError as e:
            return {"message": "Validation error", "error": e.to_dict()}, 400
        except NotUniqueError:
            return {"message": "A user with this email already exists", "value": user.email}, 400

        app.logger.info(f"new user created: {user.id} {user.name} <{user.email}>")
        return {"message": "User created successfully", "user": json.loads(user.to_json())}, 201


class UserApi(Resource):
    """API resource for managing individual user operations."""

    decorators = [limiter.limit("10 per minute")]

    def _get_user(self, user_id: str) -> Union[tuple[Dict, int], User]:
        """Helper method to retrieve a user by ID.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            Either a User object or an error response tuple.
        """
        try:
            return User.objects.get(id=user_id)
        except ValidationError as e:
            return {"message": e.message}, 400
        except DoesNotExist:
            return {"message": f"User with ID {user_id} not found"}, 404

    def get(self, id: str):
        """Retrieve a specific user by ID.

        Args:
            id: The ID of the user to retrieve.

        Returns:
            User data or error message.
        """
        user_or_error = self._get_user(id)
        user = user_or_error if isinstance(user_or_error, User) else None

        if not user:
            return user_or_error

        return Response(user.to_json(), mimetype="application/json", status=200)

    def put(self, id: str):
        """Update a specific user by ID.

        Args:
            id: The ID of the user to update.

        Returns:
            Response message with updated user data or error.
        """
        data = request.get_json()

        user_or_error = self._get_user(id)
        user = user_or_error if isinstance(user_or_error, User) else None

        if not user:
            return user_or_error

        try:
            user.update(**data)
            user.validate()
            if "password" in data:
                user.hash_password()
            user.save()
        except ValidationError as e:
            return {"message": "Validation error", "error": e.to_dict()}, 400
        except NotUniqueError:
            return {"message": "A user with this email already exists", "value": data.get("email")}, 400

        updated_user = User.objects.get(id=id)
        app.logger.info(f"user updated: {user.id} {user.name} <{user.email}>")
        return {"message": "User updated successfully", "user": json.loads(updated_user.to_json())}, 200

    def delete(self, id: str):
        """Delete a specific user by ID.

        Args:
            id: The ID of the user to delete.

        Returns:
            Response message with deleted user data or error.
        """

        user_or_error = self._get_user(id)
        user = user_or_error if isinstance(user_or_error, User) else None

        if not user:
            return user_or_error

        user_data = json.loads(user.to_json())
        user.delete()

        app.logger.info(f"user deleted: {user.id}")
        return {"message": "User deleted successfully", "user": user_data}, 200
