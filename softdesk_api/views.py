from rest_framework.views import APIView
from rest_framework.response import Response
 
from softdesk_api.models import Projects
from softdesk_api.serializers import ProjectsSerializer
 
class ProjectsAPIView(APIView):
 
    def get(self, *args, **kwargs):
        projects = Projects.objects.all()
        serializer = ProjectsSerializer(projects, many=True)
        return Response(serializer.data)


from rest_framework.viewsets import ReadOnlyModelViewSet
 
class CategoryViewset(ReadOnlyModelViewSet):
 
    serializer_class = ProjectsSerializer
 
    def get_queryset(self):
        return Projects.objects.all()