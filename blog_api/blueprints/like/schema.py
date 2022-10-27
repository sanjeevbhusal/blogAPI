from marshmallow import Schema, fields


class LikeResponseSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    post_id = fields.Int(required=True)
