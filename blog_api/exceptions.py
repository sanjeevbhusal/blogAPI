class TokenDoesnotExistError(Exception):
    code = 401
    description = "token doesnot exist. please provide token with every request to authorize yourself"


class InvalidTokenError(Exception):
    code = 401
    description = "token is invalid. please provide correct token with every request to authorize yourself"
