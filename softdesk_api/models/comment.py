from __future__ import annotations

from django.conf import settings
from django.db import models
from rest_framework.exceptions import NotFound, PermissionDenied


class Comment(models.Model):
    description = models.CharField(max_length=250)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    issue_id = models.ForeignKey(to="softdesk_api.Issue", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_comment(comment_id: int) -> Comment:
        """
        Raising error if comment doesn't exist else return comment
        """
        comment = Comment.objects.filter(pk=comment_id).first()

        if not comment:
            raise NotFound(detail="The comment id does not exists")
        return comment

    def is_in_issue(self, issue: Issue) -> None:
        """
        Raising error if comment doesn't in issue
        """

        if self.issue_id != issue:
            raise NotFound(detail="The comment is not part of this issue")

    def is_author(self, user: User) -> None:
        """
        Raising error if user isn't author of comment
        """
        if self.author_user_id.id != user.id:
            raise PermissionDenied(detail="You must be the author of the comment")
