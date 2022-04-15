from rest_framework.serializers import ModelSerializer
 
from softdesk_api.models import Project
 
class ProjectSerializer(ModelSerializer):
    """
    Serializer of the Project model that restricts to the fields
    id, title, description and type of project.
    """
 
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'project_type'] #'__all__' # Prendre tous les champs
        #exclude = ['author_user_id']