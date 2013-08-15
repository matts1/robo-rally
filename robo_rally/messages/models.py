from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import simplejson as json
import urllib
import urllib2
from robo_rally.game.models import Lobby


def send_event(event_type, event_data):
    to_send = {
        'event': event_type,
        'data': event_data
    }
    urllib2.urlopen(settings.ASYNC_BACKEND_URL, urllib.urlencode(to_send)) 


class Message(models.Model):
    user = models.ForeignKey(User, null=True)
    lobby = models.ForeignKey(Lobby)
    action = models.TextField()
    text = models.TextField()
    created_at = models.DateTimeField(u"created at", auto_now_add=True)

    class Meta:
        ordering = ('-id',)

    def __unicode__(self):
        return "%s" % (self.text,)

    def as_dict(self):
        send_to = settings.VALID_ACTIONS[self.action]
        if send_to != settings.NONE:
            players = self.lobby.players()
            if send_to == settings.NON_SELF and self.user in players:
                players = players.exclude(username=self.user.username)
            elif send_to == settings.SELF:
                players = [self.user]

            if players:
                data = {
                    'user': self.user.username if self.user is not None else '',
                    'action': self.action,
                    'text': self.text,
                    'players': " ".join(p.username for p in players),
                }
                return json.dumps(data)

    def save(self, *args, **kwargs):
        as_dict = self.as_dict()
        super(Message, self).save(*args, **kwargs)
        if as_dict is not None:
            print 'Sending message', as_dict
            send_event('message-create', as_dict)
