from flask import Blueprint, request
from blog_api.blueprints.post.models import Post
from blog_api.utils import authentication_required, owner_required

post = Blueprint("post", __name__, url_prefix="/posts")


@post.route("/")
def get_all_posts():
    posts = Post.get_all_posts()
    return {"posts": posts}, 200


@post.route("/new", methods=["POST"])
@authentication_required
def create_post(user):
    post_details = request.form
    Post(**post_details, user_id=user.id).save()
    return {"message": "Post created"}, 201


@post.route("/<int:post_id>", methods=["PUT"])
@authentication_required
@owner_required
def update_post(existing_post, user, post_id):
    updated_details = request.form
    if updated_details.get("title"):
        existing_post.title = updated_details["title"]
    if updated_details.get("body"):
        existing_post.body = updated_details["body"]
    Post().update()
    return {"message": "Post updated"}, 201


@post.route("/<int:post_id>", methods=["DELETE"])
@authentication_required
@owner_required
def delete_post(existing_post, user, post_id):
    existing_post.delete()
    return {"message": "post was successfully deleted."}, 200



