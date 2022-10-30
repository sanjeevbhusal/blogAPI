from datetime import datetime
from typing import List

from blog_api import db


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.String(), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    comments = db.relationship("Comment", backref="post")
    likes = db.relationship("Like", backref="post")

    @classmethod
    def find_all(cls) -> List["Post"]:
        return cls.query.order_by(Post.created_time.desc()).all()

    @classmethod
    def find_limited(cls, current_page: int, posts_per_page: int) -> List["Post"]:
        return cls.query.order_by(cls.created_time.desc()).paginate(
            page=current_page, per_page=posts_per_page, error_out=False
        )

    @classmethod
    def find_by_id(cls, _id: int) -> "Post":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
