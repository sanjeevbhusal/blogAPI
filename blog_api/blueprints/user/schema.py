from marshmallow import Schema, fields


class UserRegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    firstname = fields.Str(required=True)
    middlename = fields.Str()
    lastname = fields.Str(required=True)
    bio = fields.Str()


class UserResponseSchema(Schema):
    id = fields.Integer(required=True)
    email = fields.Email(required=True)
    firstname = fields.Str(required=True)
    middlename = fields.Str()
    lastname = fields.Str(required=True)
    bio = fields.Str()


class UserLoginSchema(Schema):
    email = fields.Email()
    password = fields.Str()
