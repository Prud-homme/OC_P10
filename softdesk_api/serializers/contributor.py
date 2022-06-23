from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from softdesk_api.models import Contributor


class ContributorSerializer(ModelSerializer):
    """
    Serializer of the Project model that restricts to the fields
    id, title, description and type of project.
    """

    class Meta:
        model = Contributor
        fields = ["user_id", "project_id", "permission"]
        validators = [
            UniqueTogetherValidator(
                queryset=Contributor.objects.all(),
                fields=["user_id", "project_id"],
                message="The user is already attached to this project.",
            )
        ]
