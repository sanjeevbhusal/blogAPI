import pytest
from flask import url_for

from blog_api import create_app, db
from blog_api.blueprints.comment.schema import CommentResponseSchema
from blog_api.blueprints.like.schema import LikeResponseSchema
from blog_api.blueprints.post.schema import PostResponseSchema
from blog_api.blueprints.user.schema import UserResponseSchema
from blog_api.config import TestingConfiguration


@pytest.fixture(scope="function")
def app():
    app = create_app(configuration=TestingConfiguration)
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app


@pytest.fixture(scope="function")
def client(app):
    yield app.test_client()


@pytest.fixture(scope="function")
def get_db():
    return db


@pytest.fixture(scope="function")
def create_token(app):
    from blog_api.utils import create_token
    return create_token


@pytest.fixture(scope="function")
def test_user(client):
    payload = {"firstname": "test firstname", "middlename": "test middlename", "lastname": "test lastname",
               "bio": "test bio", "email": "test@gmail.com", "password": "password"}
    response = client.post(url_for('user.register'), data=payload)
    response_data = response.get_json()

    assert response.status_code == 201
    assert UserResponseSchema().load(response_data)
    return dict(**response_data, password=payload["password"])


@pytest.fixture(scope="function")
def test_post(client, test_user, create_token):
    auth_token = create_token(payload={'user_id': test_user['id']})
    payload = {"title": "test post", "body": "test body"}
    response = client.post(url_for('post.create_post'), data=payload, headers={"Authorization": auth_token})
    response_data = response.get_json()

    assert response.status_code == 201
    assert PostResponseSchema().load(response_data)
    return {'post_data': response_data, "user_id": test_user['id']}


@pytest.fixture(scope="function")
def test_comment(client, test_post, create_token):
    post_id = test_post["post_data"].get('id')
    user_id = test_post["user_id"]
    auth_token = create_token(payload={"user_id": user_id})
    payload = {"message": "this is a test comment"}

    expected_status_code = 201
    response = client.post(url_for("comment.create_new_comment", post_id=post_id), json=payload,
                           headers={"Authorization": auth_token})
    response_data = response.get_json()

    assert response.status_code == expected_status_code
    assert CommentResponseSchema().load(response_data)

    return {"post_id": post_id, "user_id": user_id, **response_data}


@pytest.fixture(scope="function")
def test_like(client, test_post, create_token):
    user_id = test_post["user_id"]
    post_id = test_post["post_data"].get("id")
    auth_token = create_token(payload={"user_id": user_id})

    expected_status_code = 201
    response = client.post(url_for("like.add_like_to_post", post_id=post_id), headers={"Authorization": auth_token})
    response_data = response.get_json()

    assert response.status_code == expected_status_code
    assert LikeResponseSchema().load(response_data)

    return {"post_id": post_id, "user_id": user_id, **response_data}
