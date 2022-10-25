from blog_api import db


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)
    author_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_by_id(cls, _id):
        return Comment.query.filter_by(id=_id).first()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls, post_id):
        return db.session.query(post_id=post_id).all()
