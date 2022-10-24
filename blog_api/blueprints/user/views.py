from flask import Blueprint, abort
from blog_api.blueprints.user.models import User
from blog_api.utils import create_token
from blog_api.blueprints.user.schema import UserRegisterRequestModel, UserRegisterResponseModel, UserLoginRequestModel, \
    UserLoginResponseModel
from flask_pydantic import validate

user = Blueprint("user", __name__)


@user.post("/register")
@validate(on_success_status=201)
def register(form: UserRegisterRequestModel):
    existing_user = User.get_by_email(form.email)
    if existing_user:
        abort(409, "The email is already registered.")
    User(**form.dict()).save()
    return UserRegisterResponseModel(message="User successfully registered.")


@user.post("/login")
@validate()
def login(form: UserLoginRequestModel):
    existing_user = User.get_by_email(form.email)
    if not existing_user:
        abort(404, "The email is not registered.")
    password_authenticated = existing_user.authenticate(form.password)
    if not password_authenticated:
        abort(401, "The password is incorrect")
    token = create_token({"user_id": existing_user.id})
    return UserLoginResponseModel(token=token)
