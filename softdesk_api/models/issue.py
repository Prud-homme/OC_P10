from django.db import models
from django.conf import settings
from .project import Project
from enum import Enum


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

