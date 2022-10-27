from flask import Flask
from blog_api.exceptions import ApiError
from blog_api.config import DevelopmentConfiguration
from blog_api.extensions import db, enable_foreign_key, register_error_handler


def create_app(configuration=DevelopmentConfiguration):
    app = Flask(__name__)
    app.config.from_object(configuration)
    db.init_app(app)

    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        enable_foreign_key(app)

    from blog_api.blueprints import user, post, comment, like
    app.register_blueprint(user)
    app.register_blueprint(post)
    app.register_blueprint(comment)
    app.register_blueprint(like)

    register_error_handler(app)
    return app
