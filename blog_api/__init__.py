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


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    db.init_app(app)

    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        enable_foreign_key(app)

    from blog_api.blueprints import user, post
    app.register_blueprint(user)
    app.register_blueprint(post)

    with app.app_context():
        db.session.execute('pragma foreign_keys=on')
        # db.drop_all()
        db.create_all()

    return app
