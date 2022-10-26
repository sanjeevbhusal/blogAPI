class CommentDoesnotExistError(Exception):
    code = 404
    description = "The comment you are looking for doesnot exist"


class NotCommentOwnerError(Exception):
    code = 403
    description = "You don't have permission for this operation"
