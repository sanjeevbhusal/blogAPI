import os
from blog_api import create_app, db
import pytest

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.getcwd() + "/instance/test_database.db"

print(os.getcwd() + "/instance/test_database.db")


@pytest.fixture(scope="class")
def client():
    app = create_app(database_url=SQLALCHEMY_DATABASE_URI)
    app.config.update({"TESTING": True})
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield app.test_client()
    # os.remove(os.getcwd() + "/instance/test_database.db")


@pytest.fixture(scope="module")
def get_db():
    return db


@pytest.fixture(scope="class")
def test_user(client):
    user_data = {"firstname": "sanjeev", "lastname": "bhusal", "bio": "hello this is my bio",
                 "email": "bhusalsanjeev23@gmail.com", "password": "password"}
    response = client.post("/register", data=user_data)
    assert response.status_code == 201
    new_user = response.get_json()
    new_user["password"] = user_data["password"]
    return new_user
