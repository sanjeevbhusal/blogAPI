from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from blog_api.exceptions import ApiError
from marshmallow.exceptions import ValidationError

load_dotenv()
db = SQLAlchemy()


def enable_foreign_key(app):
    # Ensure FOREIGN KEY for sqlite3
    with app.app_context():
        from sqlalchemy import event
        event.listen(db.engine, 'connect', lambda c, _: c.execute('pragma foreign_keys=ON'))


def create_app(database_url="sqlite:///database.db"):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    db.init_app(app)

    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        enable_foreign_key(app)

    from blog_api.blueprints import user, post, comment, like
    app.register_blueprint(user)
    app.register_blueprint(post)
    app.register_blueprint(comment)
    app.register_blueprint(like)

    with app.app_context():
        db.session.execute('pragma foreign_keys=on')
        # db.drop_all()
        db.create_all()

    register_error(app)

    return app


def register_error(app):
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
