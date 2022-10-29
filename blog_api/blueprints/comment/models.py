from datetime import datetime

from blog_api import db


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_limited(cls, post_id, current_request, comments_per_request):
        return cls.query.filter_by(post_id=post_id).order_by(cls.created_time.desc()). \
            paginate(page=current_request, per_page=comments_per_request)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
