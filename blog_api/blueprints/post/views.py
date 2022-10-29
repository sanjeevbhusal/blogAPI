"""
modules where all the routes related to post blueprint are registered
"""

from flask import Blueprint, request

from blog_api.blueprints.post.exceptions import PostDoesnotExistError, InvalidPostAuthorError, \
    NumberOfPostToFetchNotSpecifiedError
from blog_api.blueprints.post.models import Post
from blog_api.blueprints.post.schema import PostCreateSchema, PostResponseSchema, PostUpdateSchema
from blog_api.utils import authenticate_user

post = Blueprint("post", __name__, url_prefix="/posts")


@post.get("/")
def get_all_posts():
    """
    fetch a certain amount of posts
    :return: list of posts
    """
    schema = PostResponseSchema()
    page_to_skip = request.args.get("page", None)
    posts_to_fetch = request.args.get("count", 10)

    if not posts_to_fetch:
        raise NumberOfPostToFetchNotSpecifiedError("Can't find how many post to fetch", status_code=400)

    posts = Post.get_specified_posts(page_to_skip, posts_to_fetch)
    return [schema.dump(p) for p in posts], 200


@post.post("/new")
@authenticate_user
def create_post(user):
    """
    create a new post
    :param user: user performing the operation
    :return: created post details
    """
    schema = PostCreateSchema()
    user_credentials = schema.load(request.form)

    _post = Post(**user_credentials, user_id=user.id).save()
    return PostResponseSchema().dump(_post), 201


@post.put("/<int:post_id>")
@authenticate_user
def update_post(user, post_id):
    """
    Update a single post
    :param user: user performing the operation
    :param post_id: post id
    :return: updated post details
    """
    schema = PostUpdateSchema()
    post_details = schema.load(request.form)
    existing_post = Post.find_by_id(post_id)

    if not existing_post:
        raise PostDoesnotExistError("Couldn't find your post.", status_code=404)
    if existing_post.author.id != user.id:
        raise InvalidPostAuthorError("Unauthorized access", status_code=403)

    existing_post.title = post_details.get("title") or existing_post.title
    existing_post.body = post_details.get("body") or existing_post.body
    existing_post.save()
    return PostResponseSchema().dump(existing_post), 200


@post.delete("/<int:post_id>")
@authenticate_user
def delete_post(user, post_id):
    """
    delete a single post
    :param user: user performing the operation
    :param post_id: post id
    :return: None
    """
    existing_post = Post.find_by_id(post_id)

    if not existing_post:
        raise PostDoesnotExistError("Couldn't find your post.", status_code=404)
    if existing_post.author.id != user.id:
        raise InvalidPostAuthorError("Unauthorized access", status_code=403)

    existing_post.delete()
    return "", 204
