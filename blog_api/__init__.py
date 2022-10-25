from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

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

    from blog_api.blueprints import user, post, comment
    app.register_blueprint(user)
    app.register_blueprint(post)
    app.register_blueprint(comment)

    with app.app_context():
        db.session.execute('pragma foreign_keys=on')
        # db.drop_all()
        db.create_all()

    register_error(app)

    return app


def register_error(app):
    from blog_api.blueprints.post.exceptions import PostDoesnotExistError, NotPostOwnerError
    from blog_api.blueprints.user.exceptions import UserDoesnotExistError, UserAlreadyExistError, IncorrectPasswordError
    from blog_api.blueprints.comment.exceptions import CommentDoesnotExist
    from blog_api.exceptions import TokenDoesnotExistError, InvalidTokenError

    @app.errorhandler(TokenDoesnotExistError)
    def handle_token_doesnot_exist(error):
        return {"error": error.description}, error.code

    @app.errorhandler(InvalidTokenError)
    def handle_token_doesnot_exist(error):
        return {"error": error.description}, error.code

    @app.errorhandler(PostDoesnotExistError)
    def handle_post_doesnot_exist(error):
        return {"error": error.description}, error.code

    @app.errorhandler(NotPostOwnerError)
    def handle_post_owner_invalid(error):
        return {"error": error.description}, error.code

    @app.errorhandler(UserDoesnotExistError)
    def handle_user_doesnot_exist(error):
        return {"error": error.description}, error.code

    @app.errorhandler(UserAlreadyExistError)
    def handle_user_already_exist(error):
        return {"error": error.description}, error.code

    @app.errorhandler(IncorrectPasswordError)
    def handle_authorization_required(error):
        return {"error": error.description}, error.code

    @app.errorhandler(CommentDoesnotExist)
    def handle_comment_doesnot_exist(error):
        return {"error": error.description}, error.code
