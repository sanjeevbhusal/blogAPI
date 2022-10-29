from datetime import datetime

from blog_api import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(120), nullable=False)
    middlename = db.Column(db.String(120))
    lastname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.String(), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts = db.relationship("Post", backref="author")
    comments = db.relationship("Comment", backref="author")
    author = db.relationship("Like", backref="owner")

    @classmethod
    def find_by_email(cls, email: str) -> "User":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "User":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
