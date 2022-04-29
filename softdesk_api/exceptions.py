from rest_framework.exceptions import APIException

class ProjectNotFound(APIException):
    status_code = 404
    default_detail = 'The project id does not exists'
    default_code = 'project_not_found'

class UserNotFound(APIException):
    status_code = 404
    default_detail = 'The user id does not exists'
    default_code = 'user_not_found'

class IssueNotFound(APIException):
    status_code = 404
    default_detail = 'The issue id does not exists'
    default_code = 'issue_not_found'