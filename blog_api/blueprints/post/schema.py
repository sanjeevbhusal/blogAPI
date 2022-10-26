from marshmallow import Schema, fields
from blog_api.blueprints.comment.schema import CommentResponseSchema


class PostCreateSchema(Schema):
    title = fields.Str()
    body = fields.Str()


class PostUpdateSchema(Schema):
    title = fields.Str(required=False)
    body = fields.Str(required=False)


class LikeSchema(Schema):
    user_id = fields.Integer()
    post_id = fields.Integer()


class PostResponseSchema(Schema):
    id = fields.Integer()
    title = fields.Str()
    body = fields.Str()
    created_time = fields.Str()
    comments = fields.List(fields.Nested(CommentResponseSchema()))
    likes = fields.List(fields.Nested(LikeSchema()))
