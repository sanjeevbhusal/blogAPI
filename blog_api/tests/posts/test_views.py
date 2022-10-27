from flask import url_for
from blog_api.blueprints.post.schema import PostResponseSchema


class TestPost:

    def test_get_all_post(self, client, test_post):
        response = client.get(url_for("post.get_all_posts"))
        response_data = response.get_json()
        expected_status_code = 200

        assert response.status_code == expected_status_code
        assert PostResponseSchema(many=True).load(response_data)

    def test_create_post(self, client, create_token, test_user):
        payload = {"title": "this is my post's title", "body": "this is my post's body"}
        auth_token = create_token(payload={'user_id': test_user['id']})

        expected_status_code = 201
        response = client.post(url_for("post.create_post"), data=payload, headers={"Authorization": auth_token})
        response_data = response.get_json()

        assert response.status_code == expected_status_code
        assert PostResponseSchema().load(response_data)

    def test_update_post(self, client, create_token, test_post):
        post_detail = test_post["post_data"]
        user_id = test_post["user_id"]
        auth_token = create_token(payload={'user_id': user_id})
        payload = {"title": post_detail["title"] + "updated", "body": post_detail["body"] + "updated"}

        expected_status_code = 200
        response = client.put(url_for("post.update_post", post_id=post_detail["id"]), data=payload,
                              headers={"Authorization": auth_token})
        response_data = response.get_json()

        assert response.status_code == expected_status_code
        assert PostResponseSchema().load(response_data)

    def test_delete_post(self, client, create_token, test_post):
        post_detail = test_post["post_data"]
        user_id = test_post["user_id"]
        auth_token = create_token(payload={'user_id': user_id})

        expected_status_code = 204
        response = client.delete(
            url_for("post.delete_post", post_id=post_detail["id"]), headers={"Authorization": auth_token})
        response_data = response.get_json()

        assert response.status_code == expected_status_code
        assert response_data is None
