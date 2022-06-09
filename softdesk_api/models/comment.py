from django.conf import settings
from django.db import models

# from .issue import Issue


class Comment(models.Model):
    description = models.CharField(max_length=250)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    issue_id = models.ForeignKey(to="softdesk_api.Issue", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
