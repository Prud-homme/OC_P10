from django.db import models
from django.conf import settings


class Project(models.Model):
	BACKEND = "BCK"
	FRONTEND = "FRT"
	IOS = "IOS"
	ANDROID = "ADR"
	TYPE_CHOICES = [
	    (BACKEND, "Back-end"), 
	    (FRONTEND, "Front-end"),
	    (IOS, "iOS"),
	    (ANDROID, "Android"),
	]

	# project_id = models.IntegerField() = id dans la tablec
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=250)
	project_type = models.CharField(
        max_length=3,
        choices=TYPE_CHOICES,
    )
	author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
