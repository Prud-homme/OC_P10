from django.db import models
from django.conf import settings


class Project(models.Model):
    """
    A project has 5 fields: id, title, description, project_type, author_user_id.
    """

    BACKEND = "BCK"
    FRONTEND = "FRT"
    IOS = "IOS"
    ANDROID = "ADR"
    TYPE_CHOICES = [
        (BACKEND, "Back-end"),
        (FRONTEND, "Front-end"),
        (IOS, "iOS"),
        (ANDROID, "Android"),
    ]
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    project_type = models.CharField(
        max_length=3,
        choices=TYPE_CHOICES,
    )
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
