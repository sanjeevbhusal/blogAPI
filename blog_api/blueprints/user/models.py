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

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_email(cls, email):
        return User.query.filter_by(email=email).first()
