from datetime import datetime
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import User
from django.db import models

class Lobby(models.Model):
    name = models.TextField(unique=True)

    def players(self):
        return User.objects.filter(profile__lobby=self.id)

    def size(self):
        return len(self.players())

    def add_user(self, user):
        size = self.size()
        if size < 8:
            profile = user.get_profile()
            profile.lobby = self
            profile.index = size
            profile.last_ping = datetime.now()
            profile.save()
        else:
            return 'There can only be 8 players in a lobby'

    def __repr__(self):
        return self.name

    @classmethod
    def remove_empty_lobbies(cls):
        used = set(User.objects.values_list('profile__lobby', flat=True))
        used = used - set([None])
        cls.objects.exclude(id__in=used).delete()
