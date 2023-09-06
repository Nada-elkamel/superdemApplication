from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="users/", default="image/user.jpg")
    biography = models.TextField(blank=True)
    position = models.CharField(max_length=100,blank=True)
    studies = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, default="000-000-0000")
    def __str__(self):
        return self.user.username

class Todo(models.Model):
    datecreation = models.DateTimeField()
    createur = models.TextField()
    source = models.TextField()
    interne = models.TextField(blank=True)
    responsable = models.TextField()
    nature = models.TextField()
    tache = models.TextField()
    status = models.CharField(max_length=30)
    deadline = models.DateTimeField()
    commentaire = models.TextField(blank=True)
    def __str__(self):
        return self.tache
    def is_assigned_to_user(self, user):
        return self.responsable == user