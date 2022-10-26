from marshmallow import Schema, fields


class CommentResponseSchema(Schema):
    id = fields.Integer()
    message = fields.Str()
    post_id = fields.Integer()
    author_id = fields.Integer()


class CommentCreateSchema(Schema):
    message = fields.Str()
    post_id = fields.Integer()
    author_id = fields.Integer()
