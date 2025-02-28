import json

from flask import Response, request
from flask_restful import Resource
from mongoengine import DoesNotExist, NotUniqueError, ValidationError

from app.models import User


class UsersApi(Resource):
    def get(self):
        users = User.objects()
        user_list = [json.loads(u.to_json()) for u in users]
        return user_list, 200

    def post(self):
        data = request.get_json()

        if "name" not in data:
            return {"message": "The 'name' field is required"}, 400

        if "email" not in data:
            return {"message": "The 'email' field is required"}, 400

        if "password" not in data:
            return {"message": "The 'password' field is required"}, 400

        user: User = User(**data)
        try:
            user.validate()
            user.hash_password()
            user.save()
        except ValidationError as e:
            return {"message": "validation error", "error": e.to_dict()}, 400
        except NotUniqueError:
            return {"message": "a user with this email already exists", "value": user.email}, 400

        return {"message": "user created successfully", "user": json.loads(user.to_json())}, 201


class UserApi(Resource):
    def get(self, id: str):
        try:
            user = User.objects.get(id=id)
        except ValidationError as e:
            return {"message": e.message}, 400
        except DoesNotExist as e:
            return {"message": str(e)}, 404

        return Response(user.to_json(), mimetype="application/json", status=200)

    def put(self, id: str):
        data = request.get_json()

        try:
            user = User.objects.get(id=id)
        except ValidationError as e:
            return {"message": e.message}, 400
        except DoesNotExist as e:
            return {"message": str(e)}, 404

        try:
            user.update(**data)
            user.validate()
            if "password" in data:
                user.hash_password()
            user.save()

        except ValidationError as e:
            return {"message": "validation error", "error": e.to_dict()}, 400
        except NotUniqueError:
            return {"message": "a user with this email already exists", "value": data["email"]}, 400

        user = User.objects.get(id=id)
        return {"message": "user updated successfully", "user": json.loads(user.to_json())}, 200

    def delete(self, id: str):
        try:
            user = User.objects.get(id=id)
        except ValidationError as e:
            return {"message": e.message}, 400
        except DoesNotExist as e:
            return {"message": str(e)}, 404

        user.delete()

        return {"message": "user deleted successfully", "user": json.loads(user.to_json())}, 200
