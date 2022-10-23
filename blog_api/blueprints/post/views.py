from flask import Blueprint, request
from blog_api.blueprints.post.models import Post

post = Blueprint("post", __name__, url_prefix="/posts")


@post.route("/")
def get_all_posts():
    posts = Post.get_all_posts()
    return {"posts": posts}, 200


@post.route("/new", methods=["POST"])
def create_post():
    post_details = request.form
    Post(**post_details).save()
    return {"message": "Post created"}, 201


@post.route("/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    existing_post = Post.find_by_id(post_id)
    if not existing_post:
        return {"message": "post doesn't exist"}, 404
    updated_details = request.form
    if updated_details.get("title"):
        existing_post.title = updated_details["title"]
    if updated_details.get("body"):
        existing_post.body = updated_details["body"]
    Post().update()
    return {"message": "Post updated"}, 201


@post.route("/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    existing_post = Post.find_by_id(post_id)
    if not existing_post:
        return {"message": "post doesn't exist"}, 404
    existing_post.delete()
    return {"message": "post was successfully deleted."}, 200



