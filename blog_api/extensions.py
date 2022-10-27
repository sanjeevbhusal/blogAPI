from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from blog_api.exceptions import ApiError
from marshmallow.exceptions import ValidationError
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()


def register_error_handler(app):
    @app.errorhandler(ApiError)
    def handle_resource_doesnot_exist(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        error.messages.update({"valid_data": error.valid_data})
        response = jsonify(error.messages)
        response.status_code = 400
        return response


def enable_foreign_key(app):
    # Ensure FOREIGN KEY for sqlite3
    with app.app_context():
        from sqlalchemy import event
        event.listen(db.engine, 'connect', lambda c, _: c.execute('pragma foreign_keys=ON'))
