from django.http import HttpRequest, HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from authentication.serializers import UserInformationsSerializer


class UserInformationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest) -> HttpResponse:
        user = User.objects.filter(pk=request.user.id).first()
        serializer = UserInformationsSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
