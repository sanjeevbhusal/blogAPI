from flask import Blueprint
from blog_api.blueprints.user.models import User
from blog_api.utils import create_token
from blog_api.blueprints.user.schema import UserRegisterRequestModel, UserResponseModel, UserRegisterResponseModel, \
    UserLoginRequestModel, \
    UserLoginResponseModel
from blog_api.blueprints.user.exceptions import UserAlreadyExistError, UserDoesnotExistError, IncorrectPasswordError
from flask_pydantic import validate

user = Blueprint("user", __name__)


@user.post("/register")
@validate(on_success_status=201)
def register(form: UserRegisterRequestModel):
    existing_user = User.get_by_email(form.email)
    if existing_user:
        raise UserAlreadyExistError("The email is already registered")
    new_user = User(**form.dict())
    new_user.save()
    return UserResponseModel.from_orm(new_user)


@user.post("/login")
@validate()
def login(form: UserLoginRequestModel):
    existing_user = User.get_by_email(form.email)
    if not existing_user:
        raise UserDoesnotExistError("The email is not registered")
    password_authenticated = existing_user.authenticate(form.password)
    if not password_authenticated:
        raise IncorrectPasswordError()
    token = create_token({"user_id": existing_user.id})
    return UserLoginResponseModel(token=token)
