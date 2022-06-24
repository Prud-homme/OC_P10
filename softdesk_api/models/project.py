from __future__ import annotations

from enum import Enum

from django.conf import settings
from django.db import models
from rest_framework.exceptions import NotFound, PermissionDenied

from .contributor import Contributor


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

    @staticmethod
    def is_valid_project(project: Project) -> None:
        """
        Raising error if project doesn't exist
        """
        if not project:
            raise NotFound(detail="The project id does not exists")

    def is_contributor(self, user: User) -> Optionnal[bool]:  # noqa: F821
        """
        Raising error if user isn't a contributor of project
        """

        contributor = Contributor.objects.filter(
            project_id__exact=self, user_id__exact=user
        ).first()

        if not contributor:
            raise PermissionDenied(
                detail="You must be the author or a contributor of the project"
            )
        return True

    def is_author(self, user: User) -> None:  # noqa: F821
        """
        Raising error if user isn't the author of project
        """

        if self.author_user_id.id != user.id:
            raise PermissionDenied(detail="You must be the author of the project")
