from django.contrib.auth.models import User
from django.db import models

class Lobby(models.Model):
    name = models.TextField(primary_key=True)
    time_created = models.DateTimeField()
    # game is instance of class

class LobbyPerson(models.Model):
    user = models.ForeignKey(User, primary_key=True)
    lobby = models.ForeignKey(Lobby)
    index = models.IntegerField() # index of player in lobby
    last_ping = models.TimeField()