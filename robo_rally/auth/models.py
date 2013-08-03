from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from robo_rally.game.models import Lobby

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    activation_key = models.CharField(max_length=40, null=True)

    # they can only be in one lobby at once
    lobby = models.ForeignKey(Lobby, default=None, null=True)
    index = models.IntegerField(default=None, null=True) # index of player in lobby
    last_ping = models.TimeField(default=None, null=True)

    def ping(self):
        self.last_ping = datetime.now()
