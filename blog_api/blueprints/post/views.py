from flask import Blueprint
from blog_api.blueprints.post.models import Post
from blog_api.utils import authentication_required, owner_required
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
@authentication_required
@validate(on_success_status=201)
def create_post(user, form: RequestFormCreatePostModel):
    Post(**form.dict(), user_id=user.id).save()
    return ResponseCreatePostModel(message="Your post has been created.")


@post.put("/<int:post_id>")
@owner_required
@validate()
def update_post(form: RequestFormUpdatePostModel, existing_post, **kwargs):
    existing_post.title = form.title or existing_post.title
    existing_post.body = form.body or existing_post.body
    Post().update()
    return ResponsePostModel.from_orm(existing_post)


@post.delete("/<int:post_id>")
@owner_required
def delete_post(existing_post, **kwargs):
    existing_post.delete()
    return "", 204
