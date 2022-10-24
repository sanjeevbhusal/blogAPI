from flask import Blueprint
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
        return {"message": "The email is already registered."}, 403
    User(**form.dict()).save()
    return UserRegisterResponseModel(message="User successfully registered.")


@user.post("/login")
@validate()
def login(form: UserLoginRequestModel):
    existing_user = User.get_by_email(form.email)
    if not existing_user:
        return {"error": "The email is not registered."}, 404
    password_authenticated = existing_user.authenticate(form.password)
    if not password_authenticated:
        return {"error": "The password is incorrect"}, 401
    token = create_token({"user_id": existing_user.id})
    return UserLoginResponseModel(token=token)
