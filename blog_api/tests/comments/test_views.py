from flask import url_for

from blog_api.blueprints.comment.schema import CommentResponseSchema


class TestComment:
    def test_get_all_comments(self, client, test_comment):
        expected_status_code = 200
        response = client.get(
            url_for("comment.get_all_comments", post_id=test_comment["post_id"])
        )
        response_data = response.get_json()

        assert response.status_code == expected_status_code
        assert CommentResponseSchema(many=True).load(response_data)

    def test_get_single_comment(self, client, test_comment):
        expected_status_code = 200
        response = client.get(
            url_for("comment.get_comment_by_id", comment_id=test_comment["id"])
        )
        response_data = response.get_json()

        assert response.status_code == expected_status_code
        assert CommentResponseSchema().load(response_data)

    def test_add_comment(self, client, test_post, create_token):
        post_id = test_post["post_data"].get("id")
        user_id = test_post["user_id"]
        auth_token = create_token(payload={"user_id": user_id})
        payload = {"message": "this is a test comment"}

        expected_status_code = 201
        response = client.post(
            url_for("comment.create_new_comment", post_id=post_id),
            json=payload,
            headers={"Authorization": auth_token},
        )
        response_data = response.get_json()

        assert response.status_code == expected_status_code
        assert CommentResponseSchema().load(response_data)

    def test_update_comment(self, client, test_comment, create_token):
        comment_id = test_comment["id"]
        user_id = test_comment["user_id"]
        auth_token = create_token(payload={"user_id": user_id})
        payload = {"message": "this is a updated test comment"}

        expected_status_code = 200
        response = client.put(
            url_for("comment.update_comment", comment_id=comment_id),
            json=payload,
            headers={"Authorization": auth_token},
        )
        response_data = response.get_json()

        assert response.status_code == expected_status_code
        assert CommentResponseSchema().load(response_data)

    def test_delete_comment(self, client, test_comment, create_token):
        comment_id = test_comment["id"]
        user_id = test_comment["user_id"]
        auth_token = create_token(payload={"user_id": user_id})

        expected_status_code = 204
        response = client.delete(
            url_for("comment.delete_comment", comment_id=comment_id),
            headers={"Authorization": auth_token},
        )
        response_data = response.get_json()

        assert response.status_code == expected_status_code
        assert response_data is None
