from flask import request
from datetime import datetime, timezone, timedelta
import os
import jwt
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError
from blog_api.blueprints.user.models import User
from blog_api.blueprints.user.exceptions import UserDoesnotExistError
from blog_api.exceptions import TokenDoesnotExistError, InvalidTokenError
from functools import wraps
from typing import Callable
from blog_api.extensions import bcrypt


def hash_password(password):
    return bcrypt.generate_password_hash(password).decode("utf-8")


def check_password(hashed_password, plain_password):
    return bcrypt.check_password_hash(hashed_password, plain_password)


def create_token(payload, expiration=timedelta(days=1), algorithm="HS256"):
    secret_key = os.environ.get("SECRET_KEY")
    expiration_time = (datetime.now(tz=timezone.utc) + expiration).timestamp()
    return jwt.encode({"payload": payload, "exp": expiration_time}, secret_key, algorithm=algorithm)


def extract_token_from_request():
    token = request.headers.get("Authorization")
    if token and "Bearer" in token:
        return token.split()[1]
    return token


def validate_token(token, algorithms=None):
    if algorithms is None:
        algorithms = ["HS256"]
    try:
        return jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=algorithms)
    except (InvalidSignatureError, ExpiredSignatureError):
        return None


def authenticate_user(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = extract_token_from_request()
        if not token:
            raise TokenDoesnotExistError("access token is not present in Authorization header.", status_code=401)
        token_information = validate_token(token)
        if not token_information:
            raise InvalidTokenError("access token is invalid or have expired.", status_code=401)
        user = User.get_by_id(token_information["payload"]["user_id"])
        if user is None:
            raise UserDoesnotExistError("User associated with this token doesn't exist.", status_code=404)

        return func(user=user, *args, **kwargs)

    return wrapper
