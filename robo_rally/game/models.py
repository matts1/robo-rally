from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import utc
from robo_rally.courses.models import Course
from robo_rally.game.engine import Engine

LOBBY = 0
PICK_MAP = 1
IN_GAME = 2

class Lobby(models.Model):
    name = models.TextField(unique=True)

    # for game stage, 0=lobby, 1=pick map, 2=in game
    game_stage = models.IntegerField(default=LOBBY)
    games = {}

    def players(self):
        return User.objects.filter(profile__lobby=self.id).order_by('profile__index')

    def size(self):
        return len(self.players())

    def leader(self):
        players = self.players()
        if players:
            return players[0].username
        else:
            return ''

    def add_user(self, user):
        # stop recursive import
        from robo_rally.messages.models import Message
        if self.game_stage == 0:
            profile = user.get_profile()
            if profile.lobby is not None:
                profile.leave_lobby()
            profile.lobby = self
            profile.index = self.size()
            profile.last_ping = datetime.utcnow().replace(tzinfo=utc)
            profile.save()
            Message(
                user=user,
                lobby=self,
                action='adduser',
                text=self.leader()
            ).save()
            if self.size() == 8:
                self.goto_pickmap()

    def goto_pickmap(self):
        print 'starting game in lobby', self.name
        self.game_stage = PICK_MAP
        self.save()
        self.message(None, 'goto_pickmap', str(self.size()))

    def message(self, user, action, msg):
        # stop recursive import
        from robo_rally.messages.models import Message

        Message(user=user, lobby=self, action=action, text=msg).save()

    def remove_old_players(self):
        for player in self.players():
            if player.get_profile().is_old():
                player.get_profile().leave_lobby()

    def start_game(self, course):
        self.game_stage = IN_GAME
        Lobby.games[self.name] = Engine( # class variable (hopefully)
            Course.objects.get(filename=course),
            self.players(),
        )
        self.save()

    def get_game(self):
        print Lobby.games
        return Lobby.games.get(self.name)

    def __repr__(self):
        return self.name

    @classmethod
    def remove_empty_lobbies(cls):
        used = set(User.objects.values_list('profile__lobby', flat=True))
        used = used - set([None])
        for obj in cls.objects.exclude(id__in=used):
            if obj.name in Lobby.games:
                del Lobby.games[obj]
            obj.delete()

    @classmethod
    def joinable(cls, name):
        if cls.objects.filter(name=name.title()).exclude(game_stage=LOBBY):
            raise ValidationError("The lobby exists, but is not joinable currently")
