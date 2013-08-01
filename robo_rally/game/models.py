from django.contrib.auth.models import User
from django.db import models

class Lobby(models.Model):
    name = models.TextField(primary_key=True)
    def people(self):
        return User.objects.filter(profile__lobby=self)
    game = None # game doesn't go in table

    def __repr__(self):
        return self.name
