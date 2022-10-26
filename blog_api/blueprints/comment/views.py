from flask import Blueprint, request
from blog_api.blueprints.comment.exceptions import CommentDoesnotExistError
from blog_api.blueprints.comment.models import Comment
from blog_api.blueprints.comment.schema import CommentResponseSchema, CommentCreateSchema
from blog_api.utils import authenticate_user
from blog_api.blueprints.post.exceptions import PostIdNotSpecified

comment = Blueprint("comment", __name__, url_prefix="/comments")


@comment.get("/")
def get_all_comments():
    post_id = request.args.get("post_id")
    if not post_id:
        raise PostIdNotSpecified("specify post id query parameter to fetch a comment from a post")
    comment_list = Comment.find_by_post_id(post_id)
    schema = CommentResponseSchema()
    return [schema.dump(_comment) for _comment in comment_list]


@comment.get("/<int:comment_id>")
def get_comment_by_id(comment_id):
    existing_comment = Comment.find_by_id(comment_id)
    if not existing_comment:
        raise CommentDoesnotExistError("The post you are looking for doesnot exist")
    schema = CommentResponseSchema()
    return schema.dump(existing_comment)


@comment.post("/new")
@authenticate_user
def create_new_comment(user, ):
    schema = CommentCreateSchema()
    comment_details = schema.load(
        dict(request.json, post_id=request.args.get("post_id"), author_id=user.id))
    new_comment = Comment(**comment_details).save()
    return CommentResponseSchema().dump(new_comment)
