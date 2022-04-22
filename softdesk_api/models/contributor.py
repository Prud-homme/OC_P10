from django.db import models
from django.conf import settings
from .project import Project


class Contributor(models.Model):

    # "Contributor" en fr ?
    CONTRIBUTOR = "CONT"
    AUTHOR = "AUTH"
    PERMISSION_CHOICES = [
        (CONTRIBUTOR, "Contributor"),
        (AUTHOR, "Author"),
    ]

    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    permission = models.CharField(
        max_length=4,
        choices=PERMISSION_CHOICES,
    )
    role = models.CharField(max_length=100)
