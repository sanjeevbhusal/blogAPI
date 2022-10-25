class CommentDoesnotExistError(Exception):
    code = 404
    description = "Comment doesnot exist"


class NotCommentOwnerError(Exception):
    code = 403
    description = "you don't have permission for this operation"
