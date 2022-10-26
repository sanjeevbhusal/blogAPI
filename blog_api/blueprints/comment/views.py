from flask import Blueprint, request
from blog_api.blueprints.comment.exceptions import CommentDoesnotExistError
from blog_api.blueprints.comment.models import Comment
from blog_api.blueprints.comment.schema import CommentResponseSchema, CommentCreateSchema, CommentUpdateSchema, \
    CommentDeleteSchema
from blog_api.blueprints.post.models import Post
from blog_api.blueprints.post.exceptions import PostDoesnotExistError, NotPostOwnerError
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
    existing_post = Post.find_by_id(comment_details["post_id"])
    if not existing_post:
        raise PostDoesnotExistError(f"post with id {comment_details['post_id']} doesnot exist")
    new_comment = Comment(**comment_details).save()
    return CommentResponseSchema().dump(new_comment)


@comment.put("/<int:comment_id>")
@authenticate_user
def update_comment(user, comment_id):
    schema = CommentUpdateSchema()
    comment_details = schema.load(
        dict(request.json, comment_id=comment_id, author_id=user.id))
    existing_comment = Comment.find_by_id(comment_details["comment_id"])
    if not existing_comment:
        raise CommentDoesnotExistError("The comment you are looking for doesnot exist")
    if existing_comment.author.id != user.id:
        raise NotPostOwnerError("you don't have permission for this operation")

    existing_comment.message = comment_details["message"]
    existing_comment.save()
    return CommentResponseSchema().dump(existing_comment)


@comment.delete("/<int:comment_id>")
@authenticate_user
def delete_comment(user, comment_id):
    existing_comment = Comment.find_by_id(comment_id)
    if not existing_comment:
        raise CommentDoesnotExistError("The comment you are looking for doesnot exist")
    if existing_comment.author.id != user.id:
        raise NotPostOwnerError("you don't have permission for this operation")
    existing_comment.delete()
    return ""
