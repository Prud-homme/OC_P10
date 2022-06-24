from enum import Enum

from django.conf import settings
from django.db import models
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

    @classmethod
    def get_contributor(cls, project: "Project", user: "User") -> "Contributor":
        """
        Raising error if user doesn't contribute to project else return contributor
        """

        contributor = cls.objects.filter(
            project_id__exact=project, user_id__exact=user
        ).first()

        if not contributor:
            raise NotFound(detail="This user for this project doesn't exists")
        return contributor

    def is_author(self, project: "Project"):
        """
        Raising error
        """

        if project.author_user_id.id == self.user_id.id:
            raise PermissionDenied(
                detail="You are the author of this project, you can't delete yourself"
            )
