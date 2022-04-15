from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404, HttpResponseBadRequest
from rest_framework import status

from django.shortcuts import get_object_or_404
 
from rest_framework.permissions import IsAuthenticated

from softdesk_api.models import Project
from softdesk_api.serializers import ProjectSerializer


class ProjectAPIView(APIView):
    permission_classes = [IsAuthenticated]
 
    def get(self, request, format=None, project_id=None):
        if project_id is None:
            projects = Project.objects.filter(author_user_id__exact=request.user.id)
            serializer = ProjectSerializer(projects, many=True)
        else:
            project = get_object_or_404(Project, pk=project_id)
            serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author_user_id=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None, project_id=None):
        project = get_object_or_404(Project, pk=project_id)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save(author_user_id=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None, project_id=None):
        project = get_object_or_404(Project, pk=project_id)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)