class ApiError(Exception):
    def __init__(self, message, status_code, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        error_dict = dict(self.payload or ())
        error_dict["message"] = self.message
        return error_dict


class ResourceDoesnotExistError(ApiError):
    pass


class TokenDoesnotExistError(ApiError):
    pass


class InvalidTokenError(ApiError):
    pass
