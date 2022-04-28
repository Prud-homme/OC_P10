from django.db import models
from django.conf import settings
from enum import Enum


class ProjectType(Enum):
    """Class that defines the different types of projects"""

    BACKEND = "back-end"
    FRONTEND = "front-end"
    IOS = "iOS"
    ANDROID = "Android"

    @classmethod
    def choices(cls):
        """
        Returns a list of tuples representing the possible choices of project types
        """
        return [(key.value, key.name) for key in cls]


class Project(models.Model):
    """
    A project has 5 fields: id, title, description, project_type, author_user_id.
    """

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    project_type = models.CharField(max_length=15, choices=ProjectType.choices())
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
