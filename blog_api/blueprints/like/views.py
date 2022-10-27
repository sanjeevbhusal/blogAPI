from flask import Blueprint, request

from blog_api.blueprints.like.exceptions import AlreadyLikedError, LikeDoesnotExistError, InvalidLikeOwnerError
from blog_api.blueprints.like.schema import LikeResponseSchema
from blog_api.utils import authenticate_user
from blog_api.blueprints.post.models import Post
from blog_api.blueprints.post.schema import PostResponseSchema
from blog_api.blueprints.like.models import Like
from blog_api.blueprints.post.exceptions import PostDoesnotExistError, PostIdNotSpecified

like = Blueprint("like", __name__, url_prefix="/like")


@like.post("/")
@authenticate_user
def add_like(user):
    post_id = request.args.get("post_id")

    if not post_id:
        raise PostIdNotSpecified("Specify post id in query parameters", status_code=400)
    existing_post = Post.find_by_id(post_id)
    if not existing_post:
        raise PostDoesnotExistError("Couldn't find your post.", status_code=404)
    already_liked = Like.query.filter_by(user_id=user.id).filter_by(post_id=post_id).first()
    if already_liked:
        raise AlreadyLikedError("Cannot like a post twice", status_code=400)

    _like = Like(user_id=user.id, post_id=post_id).save()
    return LikeResponseSchema().dump(_like), 201


@like.delete("/<int:like_id>")
@authenticate_user
def delete_like(user, like_id):
    existing_like = Like.find_by_id(like_id)

    if not existing_like:
        raise LikeDoesnotExistError("Couldn't find your like.", status_code=404)
    if existing_like.owner.id != user.id:
        raise InvalidLikeOwnerError("Unauthorized Access", status_code=403)

    existing_like.delete()
    return "", 204
