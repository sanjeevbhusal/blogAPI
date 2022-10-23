from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    db.init_app(app)

    from blog_api.blueprints import user, post
    app.register_blueprint(user)
    app.register_blueprint(post)

    with app.app_context():
        db.create_all()
    return app
