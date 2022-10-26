from blog_api.exceptions import ApiError


class UserDoesnotExistError(ApiError):
    pass


class UserAlreadyExistError(ApiError):
    pass


class IncorrectPasswordError(ApiError):
    pass
