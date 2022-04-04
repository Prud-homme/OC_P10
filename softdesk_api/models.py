from django.db import models
from django.conf import settings

# Dossier models à faire

class Contributors(models.Model):
	# "Contributor" en fr ? 
	CONTRIBUTOR = "CONT"
	AUTHOR = "AUTH"
	PERMISSION_CHOICES = [
	    (CONTRIBUTOR, "Contributor"), 
	    (AUTHOR, "Author"),
	]

	user_id = models.IntegerField() # ForeignKey ?
	project_id = models.IntegerField() # ForeignKey ?
	# Permission par défaut ?
	permission = models.CharField(
        max_length=4,
        choices=PERMISSION_CHOICES,
    )
	role = models.CharField(max_length=100)

class Projects(models.Model):
	# project_id = models.IntegerField() = id dans la table
	title = models.CharField(max_length=100) # Longueur max à definir selon nous ?
	description = models.CharField(max_length=250)
	type = models.CharField(max_length=100) # Pas de problème d'appeler type ?
	author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Implementer le lien = ForeignKey ?

class Issues(models.Model):
	title = models.CharField(max_length=100)
	desc = models.CharField(max_length=250) # Renommer en description ?
	tag = models.CharField(max_length=100)
	priority = models.CharField(max_length=100)
	project_id = models.IntegerField() # ForeignKey ?
	status = models.CharField(max_length=100)
	author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author")
	assignee_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assignee")
	created_time = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
	# comment_id = models.IntegerField() = id dans la table
	description = models.CharField(max_length=250)
	author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	issue_id = models.ForeignKey(to=Issues, on_delete=models.CASCADE)
	created_time = models.DateTimeField(auto_now_add=True)