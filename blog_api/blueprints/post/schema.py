from marshmallow import Schema, fields


class PostCreateSchema(Schema):
    title = fields.Str()
    body = fields.Str()


class PostUpdateSchema(Schema):
    title = fields.Str(required=False)
    body = fields.Str(required=False)


class PostResponseSchema(Schema):
    id = fields.Integer()
    title = fields.Str()
    body = fields.Str()
    created_time = fields.Str()
