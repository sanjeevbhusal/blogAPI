from flask import url_for

from blog_api.blueprints.like.schema import LikeResponseSchema


class TestLike:
    def test_add_like(self, client, test_post, create_token):
        user_id = test_post["user_id"]
        post_id = test_post["post_data"]["id"]
        auth_token = create_token(payload={"user_id": user_id})

        expected_status_code = 201
        response = client.post(url_for("like.add_like_to_post", post_id=post_id), headers={"Authorization": auth_token})
        response_data = response.get_json()

        assert response.status_code == expected_status_code
        assert LikeResponseSchema().load(response_data)

    def test_delete_like(self, client, test_post, test_like, create_token):
        like_id = test_like["id"]
        user_id = test_like["user_id"]
        post_id = test_like["post_id"]
        auth_token = create_token(payload={"user_id": user_id})

        expected_status_code = 204
        response = client.delete(url_for("like.delete_like_from_post", like_id=like_id, post_id=post_id),
                                 headers={"Authorization": auth_token})
        response_data = response.get_json()

        assert response.status_code == expected_status_code
        assert response_data is None
