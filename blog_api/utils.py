"""
Module containing utility functions required by the application
"""

import os
from datetime import datetime, timezone, timedelta
from functools import wraps
from typing import Callable

import jwt
from flask import request
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError

from blog_api.blueprints.user.exceptions import UserDoesnotExistError
from blog_api.blueprints.user.models import User
from blog_api.exceptions import TokenDoesnotExistError, InvalidTokenError
from blog_api.extensions import bcrypt


def hash_password(password):
    """
    hashes a plain text password using bcrypt
    :param password: plain password
    :return: hashed password
    """
    return bcrypt.generate_password_hash(password).decode("utf-8")


def check_password(hashed_password, plain_password):
    """
    hashes the plain password and checks if the new hash matches the already hashed password
    :param hashed_password: already hashed password
    :param plain_password: password to hash and compare
    :return: bool
    """
    return bcrypt.check_password_hash(hashed_password, plain_password)


def create_token(payload, expiration=timedelta(days=1), algorithm="HS256"):
    """
    creates a jwt token
    :param payload: payload to encode in the token
    :param expiration: expiration time
    :param algorithm: algorithm to use while creating token
    :return: token
    """
    secret_key = os.environ.get("SECRET_KEY")
    expiration_time = (datetime.now(tz=timezone.utc) + expiration).timestamp()
    return jwt.encode({"payload": payload, "exp": expiration_time}, secret_key, algorithm=algorithm)


def extract_token_from_request():
    """
    extract the bearer token from a http request headers
    :return: token or None
    """
    token = request.headers.get("Authorization")
    if not token or "Bearer" not in token:
        return None
    return token.split()[1]


def validate_token(token, algorithms=None):
    """
    validates a token
    :param token: token
    :param algorithms: algorithm used while creating token
    :return: payload or None
    """
    if algorithms is None:
        algorithms = ["HS256"]
    try:
        return jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=algorithms)
    except (InvalidSignatureError, ExpiredSignatureError):
        return None


def authenticate_user(func: Callable) -> Callable:
    """
    Authenticate the current user performing http request to the application
    :param func: function to wrap
    :return: wrapper function
    """

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
