from django.http import HttpRequest, HttpResponse
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from softdesk_api.models import Project
from softdesk_api.serializers import ProjectSerializer


class ProjectAPIView(APIView):
    """
    This class allows to manage 5 endpoints linked to the CRUD operations.

    Two GET endpoints to display all the projects of the connected user or
    one of these projects with its id

    a POST endpoint for the creation of a project

    a PUT endpoint to update a project of the connected user

    a DELETE endpoint to delete one of the connected user's projects
    """

    permission_classes = [IsAuthenticated]

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
        elif project.author_user_id != request.user.id:
            raise PermissionDenied(detail="You must be the author of the project")
        return project

    def get(
        self, request: HttpRequest, format=None, project_id: int = None
    ) -> HttpResponse:
        """
        If no project id is provided, the method returns the list
        of all projects of the connected user with the status 200.
        If the user is not at the origin of any project, then an
        empty list will be returned.

        If the project id is valid and this project is authored by the
        connected user, the project is returned with the status 200.
        """
        if project_id is None:
            projects = Project.objects.filter(author_user_id__exact=request.user.id)
            serializer = ProjectSerializer(projects, many=True)
        else:
            project = self.search_project(project_id)
            serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest, format=None) -> HttpResponse:
        """
        If the user sends a valid title, description and project type,
        the project is added to the database.
        The project is then returned with the status 201.

        If the data entered is not valid, the input errors are returned
        with the status 400.
        """
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author_user_id=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(
        self, request: HttpRequest, format=None, project_id: int = None
    ) -> HttpResponse:
        """
        If the project id is valid and the connected user is not the
        author of this project or the project id is not valid, the
        404 error is raised.

        If the user sends a valid title, description and project type,
        the project is updated with the new data and is returned with
        the status 200.

        If the data entered is not valid, the input errors are returned
        with the status 400.
        """
        project = self.search_project(project_id)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save(author_user_id=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(
        self, request: HttpRequest, format=None, project_id: int = None
    ) -> HttpResponse:
        """
        If the project id is valid and the connected user is not the
        author of this project or the project id is not valid, the
        404 error is raised.

        Otherwise the project is deleted by returning the status 204.
        """
        project = self.search_project(project_id)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
