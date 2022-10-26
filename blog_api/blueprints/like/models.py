from blog_api import db


class Like(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    @classmethod
    def add(cls, like):
        db.session.add(like)
        db.session.commit()

    @classmethod
    def delete(cls, like):
        db.session.delete(like)
        db.session.commit()



