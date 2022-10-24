from flask import request
import os
import jwt
from jwt.exceptions import InvalidSignatureError
from blog_api.blueprints.user.models import User
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
            return {"message": "token doesn't exist."}, 401
        payload = validate_token(token)
        if not payload:
            return {"message": "token is invalid."}, 401
        user = User.get_by_id(payload["user_id"])
        if user is None:
            return {"message": "User associated with this token doesn't exist."}, 404

        return func(user=user, *args, **kwargs)

    return wrapper


def owner_required(func):
    from blog_api.blueprints.post.models import Post

    @wraps(func)
    def wrapper(*args, **kwargs):
        existing_post = Post.find_by_id(kwargs.get("post_id"))
        if not existing_post:
            return {"message": "post doesn't exist"}, 404
        if existing_post.author.id != kwargs.get("user").id:
            return {"message": "you don't have permission to delete someone else's post"}, 403

        return func(existing_post=existing_post, *args, **kwargs)

    return authentication_required(wrapper)
