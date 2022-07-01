from rest_framework.serializers import ModelSerializer

from softdesk_api.models import Issue


class IssueSerializer(ModelSerializer):
    """
    Serializer of the Issue model that restricts to the fields
    id, title, description and type of project.
    """

    class Meta:
        model = Issue
        fields = ["id", "title", "description", "tag", "priority", "status", "assignee_user_id"]
