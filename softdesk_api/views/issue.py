from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpRequest, HttpResponse
from rest_framework import status

from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated

from softdesk_api.models import Issue, Contributor
from softdesk_api.serializers import IssueSerializer


class IssueAPIView(APIView):
    """
    This class allows to manage 5 endpoints linked to the CRUD operations.

    a GET endpoint to retrieve the list of issues related to a project
    if the user is the author or a contributor of the project

    a POST endpoint to create a issue in a project
    if the user is the author or a contributor of the project

    a PUT endpoint to update a issue in a project
    if the user is the author of the project

    a DELETE endpoint to delete a issue in a project
    if the user is the author of the project
    """

    permission_classes = [IsAuthenticated]

    def get(
        self, request: HttpRequest, project_id: int, issue_id: int = None
    ) -> HttpResponse:
        """
        If the user is not an author or contributor of the project, the status 401 is returned.
        In case of an error on the issue id, the status 404 is returned.

        If the issue id is provided it will return the associated issue otherwise it will
        return all the issues of the project. The status 200 is returned in both cases.
        """
        contributors = Contributor.objects.filter(project_id__exact=project_id, user_id__exact=request.user.id)
        if len(contributors) == 0:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        issues = Issue.objects.filter(project_id__exact=project_id)
        if issue_id is None:
            serializer = IssueSerializer(issues, many=True)
        else:
            issue = get_object_or_404(issues, pk=issue_id)
            serializer = IssueSerializer(issue)
        return Response(serializer.data, status=status.HTTP_200_OK)

    