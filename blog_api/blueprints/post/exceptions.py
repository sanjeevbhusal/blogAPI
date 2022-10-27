from blog_api.exceptions import ApiError


class PostDoesnotExistError(ApiError):
    pass


class InvalidPostAuthorError(ApiError):
    pass


class PostIdNotSpecified(ApiError):
    pass
