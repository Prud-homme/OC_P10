from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models
from django.http import HttpRequest
from rest_framework.exceptions import NotFound


class UserManager(BaseUserManager):
    """User Manager that knows how to create users via email instead of username"""

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = UserManager()
    REQUIRED_FIELDS = ["first_name", "last_name", "password"]
    USERNAME_FIELD = "email"
    username = None
    email = models.EmailField("email address", blank=False, null=False, unique=True)

    @staticmethod
    def search_user(request: HttpRequest, user_id: int):
        """ """
        user = User.objects.filter(pk=user_id).first()

        if not user:
            raise NotFound(detail="The user id does not exists")
        return user
