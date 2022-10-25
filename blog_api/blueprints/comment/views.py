from flask import Blueprint, request
from flask_pydantic import validate

from blog_api.blueprints.comment.models import Comment
from blog_api.blueprints.comment.schema import CommentResponseSchema, CommentCreateSchema
from blog_api.utils import authenticate_user, get_post, get_comment

comment = Blueprint("comment", __name__, url_prefix="/comments")


@comment.get("/")
@get_post(query="post_id")
def get_all_comments(_post):
    schema = CommentResponseSchema()
    return [schema.dump(_comment) for _comment in _post.comments]


@comment.get("/<int:comment_id>")
@get_comment()
@validate()
def get_comment_by_id(_comment, comment_id):
    schema = CommentResponseSchema()
    return schema.dump(_comment)


@comment.post("/new")
@authenticate_user
@get_post(query="post_id")
def create_new_comment(user, _post):
    schema = CommentCreateSchema()
    post_details = schema.load(request.json)
    new_comment = Comment(**dict(post_details, author_id=user.id, post_id=_post.id)).save()
    return CommentResponseSchema().dump(new_comment)
