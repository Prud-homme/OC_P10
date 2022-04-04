from django.db import models
from django.conf import settings


class Project(models.Model):
	# project_id = models.IntegerField() = id dans la table
<<<<<<< HEAD
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=250)
	project_type = models.CharField(max_length=100)
	author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
=======
	title = models.CharField(max_length=100) # Longueur max à definir selon nous ?
	description = models.CharField(max_length=250)
	project_type = models.CharField(max_length=100) # Pas de problème d'appeler type ?
	author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Implementer le lien = ForeignKey ?
>>>>>>> dd1d6725ac8dda779fbb78afe41aa80ca9b79826
