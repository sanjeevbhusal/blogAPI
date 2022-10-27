from blog_api.exceptions import ApiError


class AlreadyLikedError(ApiError):
    pass


class LikeDoesnotExistError(ApiError):
    pass


class InvalidLikeOwnerError(ApiError):
    pass
