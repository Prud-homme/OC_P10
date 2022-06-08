from rest_framework.serializers import ModelSerializer

from softdesk_api.models import Contributor


class ContributorSerializer(ModelSerializer):
    """
    Serializer of the Project model that restricts to the fields
    id, title, description and type of project.
    """

    class Meta:
        model = Contributor
        fields = ["id", ]
