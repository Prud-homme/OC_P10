from django.http import HttpRequest, HttpResponse
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from softdesk_api.models import Issue, Project
from softdesk_api.serializers import IssueSerializer
from authentication.models import User


class IssueAPIView(APIView):
    """
    This class allows to manage 5 endpoints linked to the CRUD operations.

    Two GET endpoint to retrieve the list of issues related to a project
    or an issue with this id
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
        If the user is not an author or contributor of the project, the status 403 is returned.
        In case of an error on the issue id or if the project does not exist,
        the status 404 is returned.

        If the issue id is provided it will return the associated issue otherwise it will
        return all the issues of the project. The status 200 is returned in both cases.
        """
        project = Project().get_project(project_id=project_id)
        print(project)
        project.is_contributor(user=request.user)

        if issue_id is None:
            issues = Issue.objects.filter(project_id__exact=project)
            serializer = IssueSerializer(issues, many=True)
        else:
            issue = Issue.get_issue(issue_id=issue_id)
            issue.is_in_project(project=project)
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
        project = Project().get_project(project_id=project_id)
        project.is_contributor(user=request.user)

        assignee_user_id = request.data.get("assignee_user_id", None)
        if not assignee_user_id:
            assignee_user = request.user
        else:
            assignee_user = User.get_user(assignee_user_id)

        if not assignee_user:
            raise NotFound(detail="The user id doesn't exists and cannot be assigned")

        data = {
            "title": request.data.get("title"),
            "description": request.data.get("description"),
            "tag": request.data.get("tag"),
            "priority": request.data.get("priority"),
            "project_id": project,
            "status": request.data.get("status"),
            "assignee_user_id": assignee_user.id,
        }

        serializer = IssueSerializer(data=data)
        if serializer.is_valid():
            serializer.save(
                project_id=project,
                author_user_id=request.user,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: HttpRequest, project_id: int, issue_id: int) -> HttpResponse:
        """
        If the user is not author of the project, the status 403 is returned.
        In case of an error on the issue id, assignee user id or if the project
        does not exist, the status 404 is returned.

        If the user sends a valid data, the issue is updated with the new data
        and is returned with the status 200.

        If the data entered is not valid, the input errors are returned
        with the status 400.
        """
        project = Project().get_project(project_id=project_id)
        project.is_contributor(user=request.user)

        issue = Issue.get_issue(issue_id=issue_id)
        issue.is_in_project(project=project)
        issue.is_author(user=request.user)

        assignee_user_id = request.data.get("assignee_user_id", None)
        if not assignee_user_id:
            assignee_user = issue.assignee_user_id
        else:
            assignee_user = User.get_user(assignee_user_id)

        if not assignee_user:
            raise NotFound(detail="The user id doesn't exists and cannot be assigned")

        serializer = IssueSerializer(issue, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(
        self, request: HttpRequest, project_id: int, issue_id: int
    ) -> HttpResponse:
        """
        If the user is not author of the project, the status 403 is returned.
        In case of an error on the issue id or if the project does not exist,
        the status 404 is returned.

        Otherwise the issue is deleted by returning the status 204.
        """
        project = Project().get_project(project_id=project_id)
        project.is_contributor(user=request.user)

        issue = Issue.get_issue(issue_id=issue_id)
        issue.is_in_project(project=project)
        issue.is_author(user=request.user)

        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
