from blog_api.exceptions import ApiError


class CommentDoesnotExistError(ApiError):
    pass


class NotCommentOwnerError(ApiError):
    pass
