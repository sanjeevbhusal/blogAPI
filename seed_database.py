"""
module to create and seed the database with predefined user, post, comment and like for development purpose
"""
import sys
import warnings

warnings.filterwarnings("ignore")
from blog_api import create_app, db
from blog_api.blueprints.comment.models import Comment
from blog_api.blueprints.like.models import Like
from blog_api.blueprints.post.models import Post
from blog_api.blueprints.user.models import User
from blog_api.utils import hash_password

def seed_test_data():
    """
    data used to seed the database
    :return: None
    """
    user1_data = {
        "firstname": "sanjeev",
        "lastname": "bhusal",
        "email": "bhusalsanjeev23@gmail.com",
        "password": hash_password("password"),
        "bio": "hello my name is sanjeev. i like programming",
    }
    user1 = User(**user1_data)
    user1.save_to_db()

    post1_data = {
        "title": "my first post",
        "body": "hello this is my first post.",
        "user_id": user1.id,
    }
    post1 = Post(**post1_data)
    post1.save_to_db()

    comment1_data = {
        "message": "my first comment",
        "author_id": user1.id,
        "post_id": post1.id,
    }
    comment1 = Comment(**comment1_data)
    comment1.save_to_db()

    like1_data = {"user_id": user1.id, "post_id": post1.id}
    like1 = Like(**like1_data)
    like1.save_to_db()


def main(seed_data=False):
    """
    creates all tables in the database and seed them with predefined data
    :return:
    """
    app = create_app()
    with app.app_context():
        print("creating tables....")
        db.drop_all()
        db.create_all()
        print("tables created successfully")
        if seed_data:
            print("seeding tables....")
            seed_test_data()
            print("tables seeded successfully....")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "seed":
        main(seed_data=True)
    else:
        main()
