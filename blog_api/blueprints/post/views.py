from flask import Blueprint, request
from blog_api.blueprints.post.models import Post
from blog_api.utils import authenticate_user
from blog_api.blueprints.post.schema import PostCreateSchema, PostResponseSchema, PostUpdateSchema
from blog_api.blueprints.post.exceptions import PostDoesnotExistError

post = Blueprint("post", __name__, url_prefix="/posts")


@post.get("/")
def get_all_posts():
    schema = PostResponseSchema()
    posts = Post.get_all_posts()
    return [schema.dump(p) for p in posts]


@post.post("/new")
@authenticate_user
def create_post(user):
    schema = PostCreateSchema()
    user_credentials = schema.load(request.form)
    _post = Post(**user_credentials, user_id=user.id).save()
    return schema.dump(_post)


@post.put("/<int:post_id>")
@authenticate_user
def update_post(user, post_id):
    schema = PostUpdateSchema()
    post_details = schema.load(request.form)
    existing_post = Post.find_by_id(post_id)
    if not existing_post:
        raise PostDoesnotExistError("The post you are looking for doesnot exist")

    existing_post.title = post_details.get("title") or existing_post.title
    existing_post.body = post_details.get("body") or existing_post.body
    existing_post.save()
    return PostResponseSchema().dump(existing_post)


@post.delete("/<int:post_id>")
@authenticate_user
def delete_post(user, post_id):
    existing_post = Post.find_by_id(post_id)
    if not existing_post:
        raise PostDoesnotExistError("The post you are looking for doesnot exist")
    existing_post.delete()
    return "", 204
