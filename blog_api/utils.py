from flask import request, abort
import os
import jwt
from jwt.exceptions import InvalidSignatureError
from blog_api.blueprints.user.models import User
from blog_api.blueprints.user.exceptions import UserDoesnotExistError
from blog_api.exceptions import TokenDoesnotExistError, InvalidTokenError
from functools import wraps


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


def authentication_required(func):
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


def owner_required(func):
    from blog_api.blueprints.post.models import Post
    from blog_api.blueprints.post.exceptions import PostDoesnotExistError, NotPostOwnerError

    @wraps(func)
    def wrapper(*args, **kwargs):
        existing_post = Post.find_by_id(kwargs.get("post_id"))
        if not existing_post:
            raise PostDoesnotExistError()
        if existing_post.author.id != kwargs.get("user").id:
            raise NotPostOwnerError()

        return func(existing_post=existing_post, *args, **kwargs)

    return authentication_required(wrapper)
