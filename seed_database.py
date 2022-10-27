from blog_api import create_app, db
from blog_api.blueprints.user.models import User
from blog_api.blueprints.post.models import Post
from blog_api.blueprints.comment.models import Comment
from blog_api.blueprints.like.models import Like


def seed_test_data():
    user1_data = {"firstname": "sanjeev", "lastname": "bhusal", "email": "bhusalsanjeev23@gmail.com",
                  "password": "password", "bio": "hello my name is sanjeev. i like programming"}
    user1 = User(**user1_data).save()

    post1_data = {"title": "my first post", "body": "hello this is my first post.", "user_id": user1.id}
    post1 = Post(**post1_data).save()

    comment1_data = {"message": "my first comment", "author_id": user1.id, "post_id": post1.id}
    post1 = Comment(**comment1_data).save()

    like1_data = {"user_id": user1.id, "post_id": post1.id}
    like1 = Like(**like1_data).save()


def main():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_test_data()


if __name__ == "__main__":
    main()