from flask import Blueprint, request
from blog_api.blueprints.user.models import User
user = Blueprint("user", __name__)


@user.route("/register", methods=["POST"])
def register():
    data = request.form
    existing_user = User.get_by_email(data["email"])
    if existing_user:
        return {"message": "The email is already registered."}, 403
    User(**data).save()
    return{"message": "User successfully registered."}, 200
