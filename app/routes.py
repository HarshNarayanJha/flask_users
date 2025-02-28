from flask import Blueprint, Response, request

from app.models import User

api_bp = Blueprint("api", __name__)


@api_bp.route("/users", methods=["GET"])
def get_users():
    users = User.objects().to_json()
    return Response(users, mimetype="application/json", status=200)


@api_bp.route("/users/<string:id>", methods=["GET"])
def get_user(id: str):
    user = User.objects.get(id=id).first()
    return Response(user.to_json(), mimetype="application/json", status=200)


@api_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    user = User(**data).save()
    return Response(user.to_json(), mimetype="application/json", status=201)


@api_bp.route("/users/<string:id>", methods=["PUT"])
def update_user(id: str):
    data = request.get_json()
    user = User.objects().get(id=id).first()
    user.update(**data)
    return Response(user.to_json(), mimetype="application/json", status=200)


@api_bp.route("/users/<string:id>", methods=["DELETE"])
def delete_user(id: str):
    user = User.objects().get(id=id).first()
    user.delete()
    return Response(user.to_json(), mimetype="application/json", status=200)
