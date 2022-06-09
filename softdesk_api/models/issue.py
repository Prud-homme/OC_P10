from enum import Enum

from django.conf import settings
from django.db import models
from django.http import HttpRequest
from rest_framework.exceptions import NotFound, PermissionDenied

from .project import Project


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
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
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

    @staticmethod
    def search_issue(request: HttpRequest, project: Project, issue_id: int, must_be_author: bool = False):
        """
        Return the issue linked to the provided id
        if the id corresponds to a issue in the database and
        if the user who is connected is the author or a contributor
        Otherwise an error code is raised.

        404: the issue_id is not valid
        403: the connected user isn't the author of this issue
        """
        issue = Issue.objects.filter(pk=issue_id).first()

        if not issue:
            raise NotFound(detail="The issue id does not exists")
        elif issue.project_id != project:
            raise NotFound(detail="The issue is not part of this project")
        elif must_be_author and issue.author_user_id != request.user:
            raise PermissionDenied(detail="You must be the author of the issue")
        return issue
