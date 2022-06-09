from django.http import HttpRequest, HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from softdesk_api.models import Comment
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
        """
        """
        pass

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        """
        pass

    def put(self, request: HttpRequest) -> HttpResponse:
        """
        """
        pass

    def delete(self, request: HttpRequest) -> HttpResponse:
        """
        """
        pass