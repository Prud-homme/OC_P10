from django.contrib.auth.models import AbstractUser
from django.db import models


# pas d'username donc connexion par email ?
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name", "password"]