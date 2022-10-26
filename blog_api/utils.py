from flask import request
from datetime import datetime, timezone, timedelta
import os
import jwt
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError
from blog_api.blueprints.user.models import User
from blog_api.blueprints.user.exceptions import UserDoesnotExistError
from blog_api.exceptions import TokenDoesnotExistError, InvalidTokenError, ResourceDoesnotExistError
from functools import wraps
from typing import Callable


def create_token(payload, algorithm="HS256", days=1):
    expiration_time = (datetime.now(tz=timezone.utc) + timedelta(days=days))
    expiration_unix_timestamp = int(expiration_time.timestamp())
    secret_key = os.environ.get("secret_key")
    payload_with_expiration = {"payload": payload, "exp": expiration_unix_timestamp}
    return jwt.encode(payload_with_expiration, secret_key, algorithm=algorithm)


def extract_token_from_request():
    bearer_token = request.headers.get("Authorization")
    return bearer_token.split()[1] if bearer_token else None


def validate_token(token, algorithms=None):
    if algorithms is None:
        algorithms = ["HS256"]
    try:
        return jwt.decode(token, os.environ.get("secret_key"), algorithms=algorithms)
    except (InvalidSignatureError, ExpiredSignatureError):
        return None


def authenticate_user(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = extract_token_from_request()
        if not token:
            raise TokenDoesnotExistError("access token is not present in Authorization header.", status_code=401)
        payload = validate_token(token)
        if not payload:
            raise InvalidTokenError("access token is invalid or have expired.", status_code=401)
        user = User.get_by_id(payload["user_id"])
        if user is None:
            raise UserDoesnotExistError("User associated with this token doesn't exist.", status_code=404)

        return func(user=user, *args, **kwargs)

    return wrapper
