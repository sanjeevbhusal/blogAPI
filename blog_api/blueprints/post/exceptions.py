class PostDoesnotExistError(Exception):
    code = 404
    description = "post doesnot exist"


class NotPostOwnerError(Exception):
    code = 403
    description = "you don't have permission for this operation"


class PostIdNotSpecified(Exception):
    code = 400
    description = "specify post id query parameter to fetch a comment from a post"
