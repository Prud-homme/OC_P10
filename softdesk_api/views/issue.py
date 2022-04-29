from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpRequest, HttpResponse
from rest_framework import status
from django.contrib.auth import get_user_model

from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated

from softdesk_api.models import Issue, Contributor, Project
from softdesk_api.serializers import IssueSerializer


from softdesk_api.exceptions import ProjectNotFound, UserNotFound

from rest_framework.exceptions import PermissionDenied



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
        In case of an error on the issue id or if the project does not exist,
        the status 404 is returned.

        If the issue id is provided it will return the associated issue otherwise it will
        return all the issues of the project. The status 200 is returned in both cases.
        """
        project = get_object_or_404(Project, pk=project_id)

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

    def post(self, request: HttpRequest, project_id: int) -> HttpResponse:
        """
        If the user is not an author or contributor of the project, the status 403 is returned.
        In case of an error on the issue id, assignee user id or if the project does not exist,
        the status 404 is returned.

        The issue is added to the database and the status 201 is returned.

        If the data entered is not valid, the input errors are returned
        with the status 400.
        """
        project = Project.objects.filter(pk=project_id).first()
        if not project:
            raise ProjectNotFound

        assignee_user_id = request.data.get('assignee_user_id', None)
        if assignee_user_id is None:
            assignee_user = request.user
        else:
            assignee_user = get_user_model().objects.filter(pk=assignee_user_id).first()
        if not assignee_user:
            raise UserNotFound

        contributor = Contributor.objects.filter(project_id__exact=project_id, user_id__exact=request.user.id).first()
        if not contributor:
            raise PermissionDenied(detail='You must be the author or a contributor of the project')

        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project_id=project, author_user_id=request.user, assignee_user_id=assignee_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    