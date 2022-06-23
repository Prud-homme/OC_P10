from django.http import HttpRequest, HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# from authentication.models import User
from softdesk_api.models import Contributor#, Project
from softdesk_api.serializers import ContributorSerializer


class ContributorAPIView(APIView):
    """ """

    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, project_id: int) -> HttpResponse:
        """
        Return a list of contributor for a project provided by it's id
        """
        contributors = Contributor.objects.filter(project_id=project_id)
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
        # project = Project.search_project(request, project_id)
        # user = User.search_user(request, user_id)

        updated_request = request.POST.copy()
        updated_request.update({"project_id": project_id, "user_id": user_id})
        print(updated_request)

        serializer = ContributorSerializer(data=updated_request)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
