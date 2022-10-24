class UserDoesnotExistError(Exception):
    code = 404
    description = "User doesnot exist"


class UserAlreadyExistError(Exception):
    code = 409
    description = "User already exist"


class IncorrectPasswordError(Exception):
    code = 401
    description = "Password is incorrect"
