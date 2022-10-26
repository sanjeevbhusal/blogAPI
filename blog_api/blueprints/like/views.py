from flask import Blueprint

from blog_api.utils import authenticate_user
from blog_api.blueprints.post.models import Post
from blog_api.blueprints.post.schema import PostResponseSchema
from blog_api.blueprints.like.models import Like
from blog_api.blueprints.post.exceptions import PostDoesnotExistError

like = Blueprint("like", __name__, url_prefix="/like")


@like.post("/<int:post_id>")
@authenticate_user
def like_a_post(user, post_id):
    existing_post = Post.find_by_id(post_id)
    if not existing_post:
        raise PostDoesnotExistError("Couldn't find your post.", status_code=404)
    already_liked = Like.query.filter_by(user_id=user.id).filter_by(post_id=post_id).first()
    if already_liked:
        Like.delete(already_liked)
    else:
        Like.add(Like(user_id=user.id, post_id=post_id))
    return PostResponseSchema().dump(existing_post)
