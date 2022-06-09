from rest_framework.serializers import ModelSerializer

from softdesk_api.models import Comment


class CommentSerializer(ModelSerializer):
    """
    Serializer of the Issue model that restricts to the fields
    id, title, description and type of project.
    """

    class Meta:
        model = Comment
        fields = ["id", "description"]
