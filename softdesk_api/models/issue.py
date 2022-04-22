from django.db import models
from django.conf import settings
from .project import Project


class Issue(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    tag = models.CharField(max_length=100)
    priority = models.CharField(max_length=100)
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author_user",
    )
    assignee_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        default=author_user_id,
        on_delete=models.CASCADE,
        related_name="assignee_user",
    )
    created_time = models.DateTimeField(auto_now_add=True)
