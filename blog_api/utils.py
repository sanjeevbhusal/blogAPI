from flask import request, abort
import os
import jwt
from jwt.exceptions import InvalidSignatureError
from blog_api.blueprints.user.models import User
from blog_api.blueprints.user.exceptions import UserDoesnotExistError
from blog_api.exceptions import TokenDoesnotExistError, InvalidTokenError
from functools import wraps
from typing import Callable


def create_token(payload, algorithm="HS256"):
    return jwt.encode(payload, os.environ.get("secret_key"), algorithm=algorithm)


def extract_token_from_request():
    bearer_token = request.headers.get("Authorization")
    return bearer_token.split()[1] if bearer_token else None


def validate_token(token, algorithms=None):
    if algorithms is None:
        algorithms = ["HS256"]
    try:
        return jwt.decode(token, os.environ.get("secret_key"), algorithms=algorithms)
    except InvalidSignatureError:
        return None


def authenticate_user(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = extract_token_from_request()
        if not token:
            raise TokenDoesnotExistError()
        payload = validate_token(token)
        if not payload:
            raise InvalidTokenError()
        user = User.get_by_id(payload["user_id"])
        if user is None:
            raise UserDoesnotExistError("User associated with this token doesn't exist")

        return func(user=user, *args, **kwargs)

    return wrapper
