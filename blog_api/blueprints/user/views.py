from flask import Blueprint, request
from blog_api.blueprints.user.models import User
user = Blueprint("user", __name__)


@user.route("/register", methods=["POST"])
def register():
    user_credentials = request.form
    existing_user = User.get_by_email(user_credentials["email"])
    if existing_user:
        return {"message": "The email is already registered."}, 403
    User(**user_credentials).save()
    return{"message": "User successfully registered."}, 200


@user.route("/login", methods=["POST"])
def login():
    user_credentials = request.form
    existing_user = User.get_by_email(user_credentials["email"])
    if not existing_user:
        return {"message": "The email is not registered."}, 404
    password_authenticated = existing_user.authenticate(user_credentials["password"])
    if not password_authenticated:
        return {"message": "The password is incorrect"}, 401
    return{"message": "User successfully authenticated."}, 200
