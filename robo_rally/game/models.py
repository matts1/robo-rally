from datetime import datetime
from django.contrib.auth.models import User
from django.db import models

LOBBY = 0
PICK_MAP = 1
IN_GAME = 2

class Lobby(models.Model):
    name = models.TextField(unique=True)

    # for game stage, 0=lobby, 1=pick map, 2=in game
    game_stage = models.IntegerField(default=LOBBY)

    def players(self):
        return User.objects.filter(profile__lobby=self.id).order_by('profile__index')

    def size(self):
        return len(self.players())

    def add_user(self, user):
        if self.game_stage == 0:
            profile = user.get_profile()
            profile.lobby = self
            profile.index = self.size()
            profile.last_ping = datetime.now()
            profile.save()
            if self.size() == 8:
                self.goto_pickmap()

    def goto_pickmap(self):
        self.game_stage = PICK_MAP
        self.save()
        self.message(None, 'goto_pickmap', str(self.size()))

    def message(self, user, action, msg):
        # stop recursive import
        from robo_rally.messages.models import Message
        Message(user=user, lobby=self, action=action, text=msg).save()

    def __repr__(self):
        return self.name

    @classmethod
    def remove_empty_lobbies(cls):
        used = set(User.objects.values_list('profile__lobby', flat=True))
        used = used - set([None])
        cls.objects.exclude(id__in=used).delete()
