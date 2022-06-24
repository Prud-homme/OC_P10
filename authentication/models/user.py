from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import NotFound

from .user_manager import UserManager


class User(AbstractUser):
    objects = UserManager()
    REQUIRED_FIELDS = ["first_name", "last_name", "password"]
    USERNAME_FIELD = "email"
    username = None
    email = models.EmailField("email address", blank=False, null=False, unique=True)

    @classmethod
    def get_user(cls, user_id: int) -> "User":
        """ """
        user = cls.objects.filter(pk=user_id).first()

        if not user:
            raise NotFound(detail="The user id does not exists")
        return user
