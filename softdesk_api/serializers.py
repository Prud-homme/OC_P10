from rest_framework.serializers import ModelSerializer
 
from softdesk_api.models import Projects
 
class ProjectsSerializer(ModelSerializer):
 
    class Meta:
        model = Projects
        fields = '__all__' # Prendre tous les champs