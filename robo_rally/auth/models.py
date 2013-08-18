from datetime import datetime, timedelta
from django.contrib.sessions.models import Session
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import utc
from robo_rally.game.models import Lobby

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    activation_key = models.CharField(max_length=40, null=True, blank=True)

    # they can only be in one lobby at once
    lobby = models.ForeignKey(Lobby, default=None, null=True, blank=True)
    index = models.IntegerField(default=None, null=True, blank=True) # index of player in lobby
    last_ping = models.DateTimeField(default=None, null=True,blank=True)

    def ping(self):
        self.last_ping = datetime.utcnow().replace(tzinfo=utc)
        self.save()

    def leave_lobby(self):
        lobby = None
        if self.lobby is not None:
            for player in self.lobby.players():
                profile = player.get_profile()
                if profile.index > self.index:
                    profile.index -= 1
                    profile.save()
            lobby = self.lobby
        self.lobby = None
        self.index = None
        self.save()
        if lobby is not None:
            lobby.message(self.user, 'deleteuser', lobby.leader())

    def is_old(self):
        assert self.last_ping is not None
        return self.last_ping + timedelta(seconds=20) < datetime.utcnow().replace(tzinfo=utc)

    def get_game_player(self):
        for player in self.lobby.get_game().players:
            if self.user == player.user:
                return player
