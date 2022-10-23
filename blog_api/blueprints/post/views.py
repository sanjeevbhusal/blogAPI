from flask import Blueprint
from blog_api.blueprints.post.models import Post

post = Blueprint("post", __name__)
