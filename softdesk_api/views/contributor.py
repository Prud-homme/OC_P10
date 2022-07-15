from django.http import HttpRequest, HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from softdesk_api.models import Contributor, Project
from softdesk_api.serializers import ContributorSerializer
from authentication.models import User


class ContributorAPIView(APIView):
    """
    This class allows to manage 3 endpoints.

    a GET endpoint to display all the contributors of a project by providing its id

    a POST endpoint to add a contributor to a project

    a DELETE endpoint to remove a contributor from a project
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, project_id: int) -> HttpResponse:
        """
        Return a list of contributor for a project provided by it's id
        """
        project = Project().get_project(project_id=project_id)
        project.is_contributor(user=request.user)
        contributors = Contributor.objects.filter(project_id=project)
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest, project_id: int, user_id: int) -> HttpResponse:
        """
        If the user sends a valid user id, project id and permission,
        the contributor is added to the database.
        The project is then returned with the status 201.

        If the data entered is not valid, the input errors are returned
        with the status 400.
        """
        project = Project().get_project(project_id=project_id)
        project.is_contributor(user=request.user)
        user = User.get_user(user_id)
        data = {"project_id": project.id, "user_id": user.id, "permission": "contributor"}
        serializer = ContributorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(
        self, request: HttpRequest, project_id: int, user_id: int
    ) -> HttpResponse:
        """
        If the user sends a valid user id and project id the contributor
        is deleted from the database.
        The status 204 is returned.
        """
        project = Project().get_project(project_id=project_id)
        project.is_author(user=request.user)
        user = User.get_user(user_id)
        contributor = Contributor.get_contributor(project, user)
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
