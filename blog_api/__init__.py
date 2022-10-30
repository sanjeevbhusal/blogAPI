from flask import Flask

from blog_api.config import DevelopmentConfiguration
from blog_api.exceptions import ApiError
from blog_api.extensions import (
    db,
    bcrypt,
    enable_foreign_key,
    register_error_handler,
    register_extensions,
)


def create_app(configuration=DevelopmentConfiguration):
    """
    creates the flask instance and registers all blueprints and extensions with the instance
    :param configuration: configuration to be applied to the application
    :return: flask app instance
    """
    app = Flask(__name__)
    app.config.from_object(configuration)

    from blog_api.blueprints import user, post, comment, like

    app.register_blueprint(user)
    app.register_blueprint(post)
    app.register_blueprint(comment)
    app.register_blueprint(like)

    register_extensions(app)
    register_error_handler(app)

    if "sqlite" in app.config["SQLALCHEMY_DATABASE_URI"]:
        enable_foreign_key(app)

    return app
