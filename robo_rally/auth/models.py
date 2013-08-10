from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from robo_rally.game.models import *

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    activation_key = models.CharField(max_length=40, null=True, blank=True)

    # they can only be in one lobby at once
    lobby = models.ForeignKey(Lobby, default=None, null=True, blank=True)
    index = models.IntegerField(default=None, null=True, blank=True) # index of player in lobby
    last_ping = models.TimeField(default=None, null=True,blank=True)

    def ping(self):
        self.last_ping = datetime.now()
        self.save()

    def leave_lobby(self):
        if self.lobby is not None:
            for player in self.lobby.players():
                profile = player.get_profile()
                if profile.index > self.index:
                    profile.index -= 1
                    profile.save()
            self.lobby.message(self.user, 'deleteuser', self.user.username)
        self.lobby = None
        self.index = None
        self.save()
