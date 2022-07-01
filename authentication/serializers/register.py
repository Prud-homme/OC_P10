from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from authentication.models import User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all(), lookup="iexact")]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[
            validate_password,
            RegexValidator(
                regex="[a-z]",
                message="The password must contain at least 1 lowercase letter, a-z.",
                code="password_no_lower",
            ),
            RegexValidator(
                regex="[A-Z]",
                message="The password must contain at least 1 uppercase letter, A-Z.",
                code="password_no_upper",
            ),
            RegexValidator(
                regex="[0-9]",
                message="The password must contain at least 1 digit, 0-9.",
                code="password_no_number",
            ),
            RegexValidator(
                regex=r"[!#$&()*+,-./:;<=>?@[\]^_`{|}~]",
                message="The password must contain at least 1 symbol: !#$&()*+,-./:;<=>?@[]^_`{|}~",
                code="password_no_symbol",
            ),
        ],
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["email", "password", "password2", "first_name", "last_name"]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user
