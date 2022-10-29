from datetime import datetime

from blog_api import db


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.String(), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comments = db.relationship("Comment", backref="post")
    likes = db.relationship("Like", backref="post")

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def update(cls):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_posts(cls):
        return Post.query.all()

    @classmethod
    def get_specified_posts(cls, page_to_skip, required_posts):
        return Post.query.filter(Post.id.desc()).offset(page_to_skip * required_posts).limit(required_posts)

    @classmethod
    def find_by_id(cls, _id):
        return Post.query.filter_by(id=_id).first()
