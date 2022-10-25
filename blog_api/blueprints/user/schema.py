from marshmallow import Schema, fields


class UserRegisterSchema(Schema):
    email = fields.Email()
    password = fields.Str()
    firstname = fields.Str()
    middlename = fields.Str()
    lastname = fields.Str()
    bio = fields.Str()


class UserResponseSchema(Schema):
    email = fields.Email()
    firstname = fields.Str()
    middlename = fields.Str()
    lastname = fields.Str()
    bio = fields.Str()


class UserLoginSchema(Schema):
    email = fields.Email()
    password = fields.Str()
