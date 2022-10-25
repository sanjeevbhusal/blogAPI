from flask import Blueprint, request
from blog_api.blueprints.post.models import Post
from blog_api.utils import authenticate_user, get_post
from blog_api.blueprints.post.schema import PostCreateSchema, PostResponseSchema, PostUpdateSchema

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
@get_post(owner_needed=True)
def update_post(user, _post, post_id):
    schema = PostUpdateSchema()
    post_details = schema.load(request.form)
    _post.title = post_details.get("title") or _post.title
    _post.body = post_details.get("body") or _post.body
    _post.save()
    return PostResponseSchema().dump(_post)


@post.delete("/<int:post_id>")
@authenticate_user
@get_post(owner_needed=True)
def delete_post(_post, user, post_id):
    _post.delete()
    return "", 204
