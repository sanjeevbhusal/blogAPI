from flask import Blueprint, request
from flask_pydantic import validate

from blog_api.blueprints.comment.exceptions import CommentDoesnotExist
from blog_api.blueprints.comment.models import Comment
from blog_api.blueprints.post.models import Post
from blog_api.blueprints.comment.schema import CommentResponse, CommentCreate
from blog_api.utils import authenticate_user, get_post

comment = Blueprint("comment", __name__, url_prefix="/comments")


@comment.get("/<int:comment_id>")
@validate()
def get_comment_by_id(comment_id):
    existing_comment = Comment.find_by_id(comment_id)
    if not existing_comment:
        raise CommentDoesnotExist()
    return CommentResponse.from_orm(existing_comment)


@comment.post("/new")
@get_post()
@validate()
def create_new_comment(user, body: CommentCreate, **kwargs):
    new_comment = Comment(**dict(body.dict(), author_id=user.id))
    new_comment.save()
    return CommentResponse.from_orm(new_comment)
