from django.db import models
from django.conf import settings
from .project import Project
from enum import Enum


class Permission(Enum):
    """Class that defines the different permissions"""

    CONTRIBUTOR = "contributeur"
    AUTHOR = "auteur"

    @classmethod
    def choices(cls):
        """Returns a list of tuples representing the possible choices of permissions"""
        return [(key.value, key.name) for key in cls]


class Contributor(models.Model):
    """
    A issue has 4 fields: id, user_id, project_id, permission, role
    """

    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    permission = models.CharField(max_length=15, choices=Permission.choices())
    role = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "project_id"],
                name="unique_user_project"
            )
        ]
