from enum import Enum

from django.conf import settings
from django.db import models
from rest_framework.exceptions import NotFound, PermissionDenied


class Tag(Enum):
    """Class that defines the different permissions"""

    BUG = "BUG"
    IMPROVEMENT = "AMÉLIORATION"
    TASK = "TÂCHE"

    @classmethod
    def choices(cls):
        """Returns a list of tuples representing the possible choices of tag"""
        return [(key.value, key.name) for key in cls]


class Priority(Enum):
    """Class that defines the different permissions"""

    LOW = "FAIBLE"
    MEDIUM = "MOYENNE"
    HIGH = "ÉLEVÉE"

    @classmethod
    def choices(cls):
        """Returns a list of tuples representing the possible choices of priority"""
        return [(key.value, key.name) for key in cls]


class Status(Enum):
    """Class that defines the different permissions"""

    TO_DO = "À faire"
    IN_PROGRESS = "En cours"
    COMPLETED = "Terminé"

    @classmethod
    def choices(cls):
        """Returns a list of tuples representing the possible choices of status"""
        return [(key.value, key.name) for key in cls]


class Issue(models.Model):
    """
    A issue has 10 fields: id, title, description, tag, priority,
    project_id, status, author_user_id, assignee_user_id, created_time.
    """

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    tag = models.CharField(max_length=15, choices=Tag.choices())
    priority = models.CharField(max_length=15, choices=Priority.choices())
    project_id = models.ForeignKey(to="softdesk_api.Project", on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=Status.choices())
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author_user",
    )
    assignee_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assignee_user",
    )
    created_time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_issue(cls, issue_id: int) -> "Issue":
        """
        Raising error if issue id doesn't exist else return issue
        """
        issue = cls.objects.filter(pk=issue_id).first()

        if not issue:
            raise NotFound(detail="The issue id does not exists")

        return issue

    def is_in_project(self, project: "Project") -> None:
        """
        Raising error if issue isn't in project provided
        """

        if self.project_id != project:
            raise NotFound(detail="The issue is not part of this project")

    def is_author(self, user: "User") -> None:
        """
        Raising error if user provided isn't author of issue
        """

        if self.author_user_id.id != user.id:
            raise PermissionDenied(detail="You must be the author of the issue")
