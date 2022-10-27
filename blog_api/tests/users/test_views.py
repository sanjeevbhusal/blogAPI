from flask import url_for
from blog_api.blueprints.user.schema import UserResponseSchema


class TestUser:

    def test_register_user(self, client):
        payload = {"firstname": "sanjeev", "middlename": "random name", "lastname": "bhusal",
                   "bio": "hello this is my bio", "email": "bhusalsanjeev23@gmail.com", "password": "password"}

        expected_status_code = 201
        response = client.post(url_for("user.register"), data=payload)
        response_data = response.get_json()

        assert response.status_code == expected_status_code
        assert UserResponseSchema().load(response_data)

    def test_login_user(self, client, test_user):
        expected_status_code = 200
        response = client.post(url_for("user.login"),
                               data={"email": test_user["email"], "password": test_user["password"]})
        response_data = response.get_json()

        assert response.status_code == expected_status_code
        assert UserResponseSchema().load(response_data["user"])
        assert response_data["token"]
