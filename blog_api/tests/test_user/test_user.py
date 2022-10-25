from blog_api.blueprints.user.exceptions import UserAlreadyExistError, IncorrectPasswordError, UserDoesnotExistError


class TestRegister:
    payload = {"firstname": "sanjeev", "lastname": "bhusal", "bio": "hello this is my bio",
               "email": "bhusalsanjeev23@gmail.com", "password": "password"}

    def test_successful_register(self, client):
        expected_status_code = 201
        response = client.post("/register", data=self.payload)
        new_user_details = response.get_json()
        assert new_user_details["email"] == self.payload["email"]
        assert response.status_code == expected_status_code

    def test_incorrect_data(self, client):
        expected_error_message, expected_status_code = "field required", 400
        incorrect_payload = {key: value for key, value in self.payload.items() if key != "email"}
        response = client.post("/register", data=incorrect_payload)
        error_details = response.get_json()
        assert response.status_code == expected_status_code
        assert "validation_error" in error_details

    def test_user_already_exist(self, client):
        expected_error_message, expected_status_code = UserAlreadyExistError.description, UserAlreadyExistError.code
        response = client.post("/register", data=self.payload)
        error_details = response.get_json()
        assert response.status_code == expected_status_code
        assert error_details["error"] == expected_error_message


class TestLogin:
    def test_successful_login(self, client, test_user):
        expected_status_code = 200
        response = client.post("/login", data={"email": test_user["email"], "password": test_user["password"]})
        assert response.status_code == expected_status_code
        assert "token" in response.get_json()

    def test_incorrect_email(self, client):
        expected_status_code, expected_error_message = UserDoesnotExistError.code, UserDoesnotExistError.description
        response = client.post("/login", data={"email": "unregisteredemail@gmail.com", "password": "password"})
        assert response.status_code == expected_status_code
        assert response.get_json()["error"] == expected_error_message

    def test_incorrect_password(self, client, test_user):
        expected_status_code, expected_error_message = IncorrectPasswordError.code, IncorrectPasswordError.description
        response = client.post("/login", data={"email": test_user["email"], "password": "wrong password"})
        assert response.status_code == expected_status_code
        assert response.get_json()["error"] == expected_error_message
