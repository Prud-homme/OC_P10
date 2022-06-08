from django.db import models
from django.conf import settings
from enum import Enum
from django.http import HttpRequest
    
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
    def search_project(request: HttpRequest, project_id: int):
        """
        Return the project linked to the provided id
        if the id corresponds to a project in the database
        and if the user who is connected is the author
        Otherwise an error code is raised.

        404: the project_id is not valid
        403: the connected user is not the author of this project
        """
        project = Project.objects.filter(pk=project_id).first()
        if not project:
            raise NotFound(detail="The project id does not exists")
        elif project.author_user_id != request.user:
            raise PermissionDenied(detail="You must be the author or a contributor of the project")
        return project

