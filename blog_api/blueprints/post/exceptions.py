from blog_api.exceptions import ApiError


class PostDoesnotExistError(ApiError):
    pass


class NotPostOwnerError(ApiError):
    pass


class PostIdNotSpecified(ApiError):
    pass
