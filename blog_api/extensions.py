"""
Extensions used in the application
"""
import os
import warnings

from dotenv import load_dotenv

from blog_api import DevelopmentConfiguration

from flask import jsonify
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from marshmallow.exceptions import ValidationError

from blog_api.exceptions import ApiError

load_dotenv()
db = SQLAlchemy()
bcrypt = Bcrypt()

if os.getenv("SECRET_KEY") is None:
    os.environ["SECRET_KEY"] = DevelopmentConfiguration.DEFAULT_SECRET_KEY
    warnings.warn(
        "Warning..........SECRET KEY environment variable is not set. Defaulting to a predefined variable defined in "
        "config "
    )


def register_error_handler(app):
    """
    registers error raised in the application and raises appropriate error handler based on error raised
    :param app: flask application instance
    :return: None
    """

    @app.errorhandler(ApiError)
    def handle_application_error(error):
        """
        this error handler gets invoked whenever an application specific(user defined) error is raised
        :param error: error object
        :return: json response
        """
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """
        this error handler gets invoked whenever SQLALCHEMY raises a validation error i.e when the input data doesnot
        satisfy the defined schema
        :param error: error object
        :return: json response
        """
        error.messages.update({"valid_data": error.valid_data})
        response = jsonify(error.messages)
        response.status_code = 400
        return response

    @app.errorhandler(Exception)
    def handle_unhandled_errors(error):
        print(error)
        response = jsonify({"error": "Oops! Something went wrong."})
        response.status_code = 400
        return response


def enable_foreign_key(app):
    """
    enable foreign key integrity if sqlite is used as a database. sqlite doesnot check for foreign key integrity by
    default
    :param app: flask application instance
    :return: none
    """
    with app.app_context():
        from sqlalchemy import event

        event.listen(
            db.engine, "connect", lambda c, _: c.execute("pragma foreign_keys=ON")
        )


def register_extensions(app):
    """
    registers extensions used in the application
    :param app: flask app instance
    :return: None
    """
    db.init_app(app)
    bcrypt.init_app(app)
