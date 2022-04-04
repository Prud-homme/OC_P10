from django.db import models
from django.conf import settings


class Project(models.Model):
	# project_id = models.IntegerField() = id dans la table
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=250)
	project_type = models.CharField(max_length=100)
	author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)