from flask import Blueprint, request
from blog_api.blueprints.comment.exceptions import CommentDoesnotExistError
from blog_api.blueprints.comment.models import Comment
from blog_api.blueprints.comment.schema import CommentResponseSchema, CommentCreateSchema, CommentUpdateSchema
from blog_api.blueprints.post.models import Post
from blog_api.blueprints.post.exceptions import PostDoesnotExistError, NotPostOwnerError
from blog_api.utils import authenticate_user
from blog_api.blueprints.post.exceptions import PostIdNotSpecified

comment = Blueprint("comment", __name__, url_prefix="/comments")


@comment.get("/")
def get_all_comments():
    post_id = request.args.get("post_id")
    if not post_id:
        raise PostIdNotSpecified("Post id is missing", status_code=400)
    comment_list = Comment.find_by_post_id(post_id)
    schema = CommentResponseSchema()
    return [schema.dump(_comment) for _comment in comment_list], 200


@comment.get("/<int:comment_id>")
def get_comment_by_id(comment_id):
    existing_comment = Comment.find_by_id(comment_id)
    if not existing_comment:
        raise CommentDoesnotExistError("Couldn't find your comment", status_code=404)
    schema = CommentResponseSchema()
    return schema.dump(existing_comment), 200


@comment.post("/new")
@authenticate_user
def create_new_comment(user, ):
    schema = CommentCreateSchema()
    comment_details = schema.load(
        dict(request.json, post_id=request.args.get("post_id"), author_id=user.id))
    existing_post = Post.find_by_id(comment_details["post_id"])
    if not existing_post:
        raise PostDoesnotExistError("Couldn't find your post", status_code=404)
    new_comment = Comment(**comment_details).save()
    return CommentResponseSchema().dump(new_comment), 201


@comment.put("/<int:comment_id>")
@authenticate_user
def update_comment(user, comment_id):
    schema = CommentUpdateSchema()
    comment_details = schema.load(
        dict(request.json, comment_id=comment_id, author_id=user.id))
    existing_comment = Comment.find_by_id(comment_details["comment_id"])
    if not existing_comment:
        raise CommentDoesnotExistError("Couldn't find your comment.", status_code=404)
    if existing_comment.author.id != user.id:
        raise NotPostOwnerError("Unauthorized access", status_code=403)

    existing_comment.message = comment_details["message"]
    existing_comment.save()
    return CommentResponseSchema().dump(existing_comment), 200


@comment.delete("/<int:comment_id>")
@authenticate_user
def delete_comment(user, comment_id):
    existing_comment = Comment.find_by_id(comment_id)
    if not existing_comment:
        raise CommentDoesnotExistError("Couldn't find your comment.", status_code=404)
    if existing_comment.author.id != user.id:
        raise NotPostOwnerError("Unauthorized access", status_code=403)
    existing_comment.delete()
    return "", 204
