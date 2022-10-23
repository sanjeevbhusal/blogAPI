from flask import Blueprint, request
from blog_api.blueprints.post.models import Post

post = Blueprint("post", __name__, url_prefix="/posts")


@post.route("/")
def get_all_posts():
    posts = Post.get_all_posts()
    return {"posts": posts}, 200


@post.route("/new", methods=["Post"])
def create_post():
    post_details = request.form
    Post(**post_details).save()
    return {"message": "Post created"}, 201
