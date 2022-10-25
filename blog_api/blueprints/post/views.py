from flask import Blueprint
from blog_api.blueprints.post.models import Post
from blog_api.utils import authenticate_user, get_post
from flask_pydantic import validate
from blog_api.blueprints.post.schema import ResponsePostModel, RequestFormUpdatePostModel, ResponseCreatePostModel, \
    RequestFormCreatePostModel

post = Blueprint("post", __name__, url_prefix="/posts")


@post.get("/")
@validate(response_many=True)
def get_all_posts():
    posts = Post.get_all_posts()
    return [ResponsePostModel.from_orm(p) for p in posts]


@post.post("/new")
@authenticate_user
@validate(on_success_status=201)
def create_post(user, form: RequestFormCreatePostModel):
    Post(**form.dict(), user_id=user.id).save()
    return ResponseCreatePostModel(message="Your post has been created.")


@post.put("/<int:post_id>")
@authenticate_user
@get_post(owner_needed=True)
@validate()
def update_post(user, _post, post_id, form: RequestFormUpdatePostModel):
    _post.title = form.title or _post.title
    _post.body = form.body or _post.body
    Post().update()
    return ResponsePostModel.from_orm(_post)


@post.delete("/<int:post_id>")
@authenticate_user
@get_post(owner_needed=True)
def delete_post(_post, user, post_id):
    _post.delete()
    return "", 204
