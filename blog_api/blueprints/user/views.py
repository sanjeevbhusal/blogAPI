from flask import Blueprint, request
from blog_api.blueprints.user.models import User
from blog_api.utils import create_token
from blog_api.blueprints.user.schema import UserRegisterSchema, UserLoginSchema, UserResponseSchema
from blog_api.blueprints.user.exceptions import UserAlreadyExistError, UserDoesnotExistError, IncorrectPasswordError

user = Blueprint("user", __name__)


@user.post("/register")
def register():
    schema = UserRegisterSchema()
    user_credentials = schema.load(request.form)
    existing_user = User.get_by_email(user_credentials["email"])

    if existing_user:
        raise UserAlreadyExistError("That email is taken. Try another.", status_code=409)

    new_user = User(**user_credentials).save()
    return UserResponseSchema().dump(new_user), 201


@user.post("/login")
def login():
    schema = UserLoginSchema(load_only=["password"])
    user_credentials = schema.load(request.form)
    existing_user = User.get_by_email(user_credentials["email"])

    if not existing_user:
        raise UserDoesnotExistError("Couldn't find your email.", status_code=404)
    password_authenticated = existing_user.authenticate(user_credentials["password"])
    if not password_authenticated:
        raise IncorrectPasswordError("Wrong password. Try again or click Forgot password to reset it.", status_code=401)

    token = create_token({"user_id": existing_user.id})
    return dict(token=token, user=UserResponseSchema().dump(existing_user)), 200
