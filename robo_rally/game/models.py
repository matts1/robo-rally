from django.contrib.auth.models import User
from django.db import models

class Lobby(models.Model):
    name = models.TextField(primary_key=True)
    game = None # game doesn't go in table

    def people(self):
        return User.objects.filter(profile__lobby=self)

    def num_people(self):
        return len(self.people())

    def __repr__(self):
        return self.name
