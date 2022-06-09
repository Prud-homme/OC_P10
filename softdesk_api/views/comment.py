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

    def get(self, request: HttpRequest) -> HttpResponse:
        """ """
        pass

    def post(self, request: HttpRequest) -> HttpResponse:
        """ """
        pass

    def put(self, request: HttpRequest, project_id: int, issue_id: int, comment_id: int) -> HttpResponse:
        """
        Update the comment if the project id and the issue id are valid.
        """
        project = Project.search_project(request, project_id)
        issue = Issue.search_issue(request, project, issue_id)
        comment = Comment.search_issue(request, issue, comment_id, must_be_author=True)

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(
                issue_id=issue,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: HttpRequest) -> HttpResponse:
        """ """
        pass
