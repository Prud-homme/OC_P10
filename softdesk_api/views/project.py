from django.http import HttpRequest, HttpResponse
from rest_framework import status
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

    def get(self, request: HttpRequest, project_id: int = None) -> HttpResponse:
        """
        If no project id is provided, the method returns the list
        of all projects of the connected user with the status 200.
        If the user is not at the origin of any project, then an
        empty list will be returned.

        If the project id is valid and this project is authored by the
        connected user, the project is returned with the status 200.
        """
        if project_id is None:
            projects = Project.objects.filter(author_user_id__exact=request.user)
            serializer = ProjectSerializer(projects, many=True)
        else:
            project = Project.search_project(request, project_id)
            serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest) -> HttpResponse:
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

    def put(self, request: HttpRequest, project_id: int = None) -> HttpResponse:
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
        project = Project.search_project(request, project_id)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: HttpRequest, project_id: int = None) -> HttpResponse:
        """
        If the project id is valid and the connected user is not the
        author of this project or the project id is not valid, the
        404 error is raised.

        Otherwise the project is deleted by returning the status 204.
        """
        project = Project.search_project(request, project_id)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
