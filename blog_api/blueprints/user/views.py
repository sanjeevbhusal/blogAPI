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
        raise UserAlreadyExistError("The email is already registered")
    new_user = User(**user_credentials).save()
    return UserResponseSchema().dump(new_user)


@user.post("/login")
def login():
    schema = UserLoginSchema(load_only=["password"])
    user_credentials = schema.load(request.form)
    existing_user = User.get_by_email(user_credentials["email"])
    if not existing_user:
        raise UserDoesnotExistError("The email is not registered")
    password_authenticated = existing_user.authenticate(user_credentials["password"])
    if not password_authenticated:
        raise IncorrectPasswordError("The password is incorrect")
    token = create_token({"user_id": existing_user.id})
    return dict(token=token, user=UserResponseSchema().dump(existing_user))
