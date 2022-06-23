from __future__ import annotations

from enum import Enum

from django.conf import settings
from django.db import models
from django.http import HttpRequest
from rest_framework.exceptions import NotFound, PermissionDenied


class Permission(Enum):
    """Class that defines the different permissions"""

    CONTRIBUTOR = "contributor"
    AUTHOR = "author"

    @classmethod
    def choices(cls):
        """Returns a list of tuples representing the possible choices of permissions"""
        return [(key.value, key.name) for key in cls]


class Contributor(models.Model):
    """
    A issue has 4 fields: id, user_id, project_id, permission, role
    """

    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(to="softdesk_api.Project", on_delete=models.CASCADE)
    permission = models.CharField(max_length=15, choices=Permission.choices())
    role = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "project_id"], name="unique_user_project"
            )
        ]

    def search_contributor(request: HttpRequest, project: Project, user: User):
        """
        Return contributor if exist in database
        """
        # from softdesk_api.models import Project
        # from authentication.models import User
        # project = Project.objects.filter(pk=project_id).first()

        contributor = Contributor.objects.filter(
            project_id__exact=project, user_id__exact=user
        ).first()
        if not contributor:
            raise NotFound(detail="This user for this project doesn't exists")
        elif project.author_user_id.id == contributor.user_id.id:
            raise PermissionDenied(
                detail="You are the author of this project, you can't delete yourself"
            )
        return contributor
