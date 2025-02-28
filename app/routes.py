import json

from flask import Blueprint, Response, jsonify, request
from mongoengine import DoesNotExist, NotUniqueError, ValidationError

from app.models import User

api_bp = Blueprint("api", __name__)


@api_bp.route("/users", methods=["GET"])
def get_users():
    users = User.objects()
    user_list = [json.loads(u.to_json()) for u in users]
    return jsonify(user_list), 200


@api_bp.route("/users/<string:id>", methods=["GET"])
def get_user(id: str):
    try:
        user = User.objects.get(id=id)
    except ValidationError as e:
        return jsonify({"message": e.message}), 400
    except DoesNotExist as e:
        return jsonify({"message": str(e)}), 404

    return Response(user.to_json(), mimetype="application/json", status=200)


@api_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if "name" not in data:
        return jsonify({"message": "The 'name' field is required"}), 400

    if "email" not in data:
        return jsonify({"message": "The 'email' field is required"}), 400

    if "password" not in data:
        return jsonify({"message": "The 'password' field is required"}), 400

    user: User = User(**data)
    try:
        user.validate()
        user.hash_password()
        user.save()
    except ValidationError as e:
        return jsonify({"message": "validation error", "error": e.to_dict()}), 400
    except NotUniqueError:
        return jsonify({"message": "a user with this email already exists", "value": user.email}), 400

    return jsonify({"message": "user created successfully", "user": json.loads(user.to_json())}), 201


@api_bp.route("/users/<string:id>", methods=["PUT"])
def update_user(id: str):
    data = request.get_json()

    try:
        user = User.objects.get(id=id)
    except ValidationError as e:
        return jsonify({"message": e.message}), 400
    except DoesNotExist as e:
        return jsonify({"message": str(e)}), 404

    try:
        user.update(**data)
        user.validate()
        if "password" in data:
            user.hash_password()
        user.save()

    except ValidationError as e:
        return jsonify({"message": "validation error", "error": e.to_dict()}), 400
    except NotUniqueError:
        return jsonify({"message": "a user with this email already exists", "value": data["email"]}), 400

    user = User.objects.get(id=id)
    return jsonify({"message": "user updated successfully", "user": json.loads(user.to_json())}), 200


@api_bp.route("/users/<string:id>", methods=["DELETE"])
def delete_user(id: str):
    try:
        user = User.objects.get(id=id)
    except ValidationError as e:
        return jsonify({"message": e.message}), 400
    except DoesNotExist as e:
        return jsonify({"message": str(e)}), 404

    user.delete()

    return jsonify({"message": "user deleted successfully", "user": json.loads(user.to_json())}), 200
