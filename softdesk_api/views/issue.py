from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpRequest, HttpResponse
from rest_framework import status
from django.contrib.auth import get_user_model

from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated

from softdesk_api.models import Issue, Contributor, Project
from softdesk_api.serializers import IssueSerializer


from rest_framework.exceptions import PermissionDenied, NotFound



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
        If the user is not an author or contributor of the project, the status 403 is returned.
        In case of an error on the issue id or if the project does not exist,
        the status 404 is returned.

        If the issue id is provided it will return the associated issue otherwise it will
        return all the issues of the project. The status 200 is returned in both cases.
        """
        project = Project.objects.filter(pk=project_id).first()
        if not project:
            raise NotFound(detail='The project id does not exists')

        contributor = Contributor.objects.filter(project_id__exact=project_id, user_id__exact=request.user.id).first()
        if not contributor:
            raise PermissionDenied(detail='You must be the author or a contributor of the project')

        issues = Issue.objects.filter(project_id__exact=project_id)
        if issue_id is None:
            serializer = IssueSerializer(issues, many=True)
        else:
            issue = Issue.objects.filter(pk=issue_id).first()
            if not issue:
                raise NotFound(detail='The issue id does not exists')
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
            raise NotFound(detail='The project id does not exists')

        assignee_user_id = request.data.get('assignee_user_id', None)
        if assignee_user_id is None:
            assignee_user = request.user
        else:
            assignee_user = get_user_model().objects.filter(pk=assignee_user_id).first()
        if not assignee_user:
            raise NotFound(detail='The user id does not exists')

        contributor = Contributor.objects.filter(project_id__exact=project_id, user_id__exact=request.user.id).first()
        if not contributor:
            raise PermissionDenied(detail='You must be the author or a contributor of the project')

        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project_id=project, author_user_id=request.user, assignee_user_id=assignee_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(
        self, request: HttpRequest, project_id: int, issue_id: int
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
        project = Project.objects.filter(pk=project_id).first()
        if not project:
            raise NotFound(detail='The project id does not exists')

        issue = Issue.objects.filter(pk=issue_id).first()
        if not issue:
            raise NotFound(detail='The issue id does not exists')

        #author = Contributor.objects.filter(project_id__exact=project_id, user_id__exact=request.user.id, permission__exact='auteur').first()
        #if not author:
        #    raise PermissionDenied(detail='You must be the author of the project')
        
        assignee_user_id = request.data.get('assignee_user_id', None)
        if assignee_user_id is None:
            assignee_user = request.user
        else:
            assignee_user = get_user_model().objects.filter(pk=assignee_user_id).first()
        if not assignee_user:
            raise NotFound(detail='The user id does not exists')

        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save(project_id=project, author_user_id=request.user, assignee_user_id=assignee_user)
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
        projects = Project.objects.filter(author_user_id__exact=request.user.id)
        project = get_object_or_404(projects, pk=project_id)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
