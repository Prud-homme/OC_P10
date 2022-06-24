from django.http import HttpRequest, HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from softdesk_api.models import Project, Issue, Comment
from softdesk_api.serializers import CommentSerializer


class CommentAPIView(APIView):
    """
    This class allows to manage 5 endpoints linked to the CRUD operations.

    Two GET endpoints to display all the comments of the connected user or
    one of these comment with its id

    a POST endpoint for the creation of a comment

    a PUT endpoint to update a comment of the connected user

    a DELETE endpoint to delete one of the connected user's comment
    """

    permission_classes = [IsAuthenticated]

    def get(
        self,
        request: HttpRequest,
        project_id: int,
        issue_id: int,
        comment_id: int = None,
    ) -> HttpResponse:
        """
        Returns all the comments of a issue if no id is sent.
        Otherwise, returns the comment associated with the id if it is valid.
        """
        project = Project().get_project(project_id=project_id)
        project.is_contributor(user=request.user)

        issue = Issue.get_issue(issue_id=issue_id)
        issue.is_in_project(project=project)

        if comment_id is None:
            comments = Comment.objects.filter(issue_id__exact=issue)
            serializer = CommentSerializer(comments, many=True)
        else:
            comment = Comment.get_comment(comment_id=comment_id)
            comment.is_in_issue(issue=issue)
            serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(
        self, request: HttpRequest, project_id: int, issue_id: int
    ) -> HttpResponse:
        """
        Add the comment to the database if the information sent is valid.
        """
        project = Project().get_project(project_id=project_id)
        project.is_contributor(user=request.user)

        issue = Issue.get_issue(issue_id=issue_id)
        issue.is_in_project(project=project)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author_user_id=request.user, issue_id=issue)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(
        self, request: HttpRequest, project_id: int, issue_id: int, comment_id: int
    ) -> HttpResponse:
        """
        Update the comment if the project id and the issue id are valid.
        """
        project = Project().get_project(project_id=project_id)
        project.is_contributor(user=request.user)

        issue = Issue.get_issue(issue_id=issue_id)
        issue.is_in_project(project=project)

        comment = Comment.get_comment(comment_id=comment_id)
        comment.is_in_issue(issue=issue)
        comment.is_author(user=request.user)

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(
                issue_id=issue,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(
        self, request: HttpRequest, project_id: int, issue_id: int, comment_id: int
    ) -> HttpResponse:
        """ """
        project = Project().get_project(project_id=project_id)
        project.is_contributor(user=request.user)

        issue = Issue.get_issue(issue_id=issue_id)
        issue.is_in_project(project=project)

        comment = Comment.get_comment(comment_id=comment_id)
        comment.is_in_issue(issue=issue)
        comment.is_author(user=request.user)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
