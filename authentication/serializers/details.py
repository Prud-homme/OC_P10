from rest_framework.serializers import ModelSerializer

from authentication.models import User


class UserInformationsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]
