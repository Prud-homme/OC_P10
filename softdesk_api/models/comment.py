from __future__ import annotations

from django.conf import settings
from django.db import models
from django.http import HttpRequest
from rest_framework.exceptions import NotFound, PermissionDenied


class Comment(models.Model):
    description = models.CharField(max_length=250)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    issue_id = models.ForeignKey(to="softdesk_api.Issue", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def search_comment(
        request: HttpRequest,
        issue: Issue,
        comment_id: int,
        must_be_author: bool = False,
    ):
        """
        Return the issue linked to the provided id
        if the id corresponds to a issue in the database and
        if the user who is connected is the author or a contributor
        Otherwise an error code is raised.

        404: the issue_id is not valid
        403: the connected user isn't the author of this issue
        """
        comment = Comment.objects.filter(pk=comment_id).first()

        if not comment:
            raise NotFound(detail="The comment id does not exists")
        elif comment.issue_id != issue:
            raise NotFound(detail="The comment is not part of this issue")
        elif must_be_author and comment.author_user_id != request.user:
            raise PermissionDenied(detail="You must be the author of the comment")
        return issue
