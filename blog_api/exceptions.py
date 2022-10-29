"""
A module where generic exceptions (not blueprint specific) are present.
"""


class ApiError(Exception):
    """
    A generic error template which is extended by other errors.
    """

    def __init__(self, message, status_code, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        error_dict = dict(self.payload or ())
        error_dict["message"] = self.message
        return error_dict


class TokenDoesnotExistError(ApiError):
    """
    Error raised when user tries to access a protected resource without token in request
    """
    pass


class InvalidTokenError(ApiError):
    """
    Error raised when token is invalid or expired """
    pass
