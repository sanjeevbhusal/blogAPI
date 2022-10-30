"""
modules where all the routes related to like blueprint are registered
"""

from flask import Blueprint, request

from blog_api.blueprints.like.exceptions import (
    AlreadyLikedError,
    LikeDoesnotExistError,
    InvalidLikeOwnerError,
)
from blog_api.blueprints.like.models import Like
from blog_api.blueprints.like.schema import LikeResponseSchema
from blog_api.blueprints.post.exceptions import (
    PostDoesnotExistError,
    PostIdNotSpecifiedError,
)
from blog_api.blueprints.post.models import Post
from blog_api.utils import authenticate_user

like = Blueprint("like", __name__, url_prefix="/like")


@like.post("/")
@authenticate_user
def add_like_to_post(user):
    """
    add a like to a post
    :param user: user performing the operation
    :return: created like details
    """
    post_id = int(request.args.get("post_id"))

    if not post_id:
        raise PostIdNotSpecifiedError(
            "Specify post id in query parameters", status_code=400
        )
    existing_post = Post.find_by_id(post_id)
    if not existing_post:
        raise PostDoesnotExistError("Couldn't find your post.", status_code=404)
    already_liked = (
        Like.query.filter_by(user_id=user.id).filter_by(post_id=post_id).first()
    )
    if already_liked:
        raise AlreadyLikedError("Cannot like a post twice", status_code=400)

    _like = Like(user_id=user.id, post_id=post_id)
    _like.save_to_db()
    return LikeResponseSchema().dump(_like), 201


@like.delete("/<int:like_id>")
@authenticate_user
def delete_like_from_post(user, like_id):
    """
    delete a like from a post
    :param user: user performing the operation
    :param like_id: like id
    :return: None
    """
    existing_like = Like.find_by_id(like_id)

    if not existing_like:
        raise LikeDoesnotExistError("Couldn't find your like.", status_code=404)
    if existing_like.owner.id != user.id:
        raise InvalidLikeOwnerError("Unauthorized Access", status_code=403)

    existing_like.delete_from_db()
    return "", 204
