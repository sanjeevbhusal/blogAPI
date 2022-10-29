"""
modules where all the routes related to user blueprint are registered
"""

from flask import Blueprint, request

from blog_api.blueprints.user.exceptions import UserAlreadyExistError, UserDoesnotExistError, IncorrectPasswordError
from blog_api.blueprints.user.models import User
from blog_api.blueprints.user.schema import UserRegisterSchema, UserLoginSchema, UserResponseSchema
from blog_api.utils import create_token, hash_password, check_password

user = Blueprint("user", __name__)


@user.post("/register")
def register():
    """
    register a user
    :return: registered user details
    """
    schema = UserRegisterSchema()
    user_credentials = schema.load(request.form)
    existing_user = User.find_by_email(user_credentials["email"])

    if existing_user:
        raise UserAlreadyExistError("That email is taken. Try another.", status_code=409)

    user_credentials["password"] = hash_password(user_credentials["password"])
    new_user = User(**user_credentials)
    new_user.save_to_db()
    return UserResponseSchema().dump(new_user), 201


@user.post("/login")
def login():
    """
    log in a user
    :return: logged in user details
    """
    schema = UserLoginSchema(load_only=["password"])
    user_credentials = schema.load(request.form)
    existing_user = User.find_by_email(user_credentials["email"])

    if not existing_user:
        raise UserDoesnotExistError("Couldn't find your email.", status_code=404)
    password_authenticated = check_password(existing_user.password, user_credentials["password"])
    if not password_authenticated:
        raise IncorrectPasswordError("Wrong password. Try again or click Forgot password to reset it.", status_code=401)

    token = create_token({"user_id": existing_user.id})
    return dict(token=token, user=UserResponseSchema().dump(existing_user)), 200


@user.get("/account/<int:user_id>")
def get_user_account(user_id):
    existing_user = User.find_by_id(user_id)
    if not existing_user:
        raise UserDoesnotExistError("Couldn't find your user", status_code=404)
    return UserResponseSchema().dump(existing_user), 200
