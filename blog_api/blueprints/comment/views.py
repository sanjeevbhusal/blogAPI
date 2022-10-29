"""
modules where all the routes related to comment blueprint are registered
"""

from flask import Blueprint, request

from blog_api.blueprints.comment.exceptions import CommentDoesnotExistError
from blog_api.blueprints.comment.models import Comment
from blog_api.blueprints.comment.schema import CommentResponseSchema, CommentCreateSchema, CommentUpdateSchema
from blog_api.blueprints.post.exceptions import PostDoesnotExistError, InvalidPostAuthorError, PostIdNotSpecified
from blog_api.blueprints.post.models import Post
from blog_api.utils import authenticate_user

comment = Blueprint("comment", __name__, url_prefix="/comments")


@comment.get("/")
def get_all_comments():
    """
    get all the comments for a particular post
    :return: list of comments
    """
    schema = CommentResponseSchema()
    post_id = request.args.get("post_id")

    if not post_id:
        raise PostIdNotSpecified("Specify post id in query parameters", status_code=400)

    comment_list = Comment.find_by_post_id(post_id)
    return [schema.dump(_comment) for _comment in comment_list], 200


@comment.get("/<int:comment_id>")
def get_comment_by_id(comment_id):
    """
    get a single comment
    :param comment_id: comment id
    :return: single comment
    """
    schema = CommentResponseSchema()
    existing_comment = Comment.find_by_id(comment_id)

    if not existing_comment:
        raise CommentDoesnotExistError("Couldn't find your comment", status_code=404)

    return schema.dump(existing_comment), 200


@comment.post("/new")
@authenticate_user
def create_new_comment(user):
    """
    create a new comment
    :param user: user performing the operation
    :return: created comment details
    """
    schema = CommentCreateSchema()
    comment_details = schema.load(dict(request.json, post_id=request.args.get("post_id"), author_id=user.id))
    existing_post = Post.find_by_id(comment_details["post_id"])

    if not existing_post:
        raise PostDoesnotExistError("Couldn't find your post", status_code=404)

    new_comment = Comment(**comment_details).save()
    return CommentResponseSchema().dump(new_comment), 201


@comment.put("/<int:comment_id>")
@authenticate_user
def update_comment(user, comment_id):
    """
    update a single comment
    :param user: user performing the operation
    :param comment_id: comment id
    :return: updated comment details
    """
    schema = CommentUpdateSchema()
    comment_details = schema.load(dict(request.json, comment_id=comment_id, author_id=user.id))
    existing_comment = Comment.find_by_id(comment_details["comment_id"])

    if not existing_comment:
        raise CommentDoesnotExistError("Couldn't find your comment.", status_code=404)
    if existing_comment.author.id != user.id:
        raise InvalidPostAuthorError("Unauthorized access", status_code=403)

    existing_comment.message = comment_details["message"]
    existing_comment.save()
    return CommentResponseSchema().dump(existing_comment), 200


@comment.delete("/<int:comment_id>")
@authenticate_user
def delete_comment(user, comment_id):
    """
    delete a single comment
    :param user: user performing the operation
    :param comment_id: comment id
    :return: None
    """
    existing_comment = Comment.find_by_id(comment_id)

    if not existing_comment:
        raise CommentDoesnotExistError("Couldn't find your comment.", status_code=404)
    if existing_comment.author.id != user.id:
        raise InvalidPostAuthorError("Unauthorized access", status_code=403)

    existing_comment.delete()
    return "", 204
