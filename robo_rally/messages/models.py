#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils import simplejson as json
import urllib
import urllib2
from django.conf import settings
from robo_rally.game.models import Lobby


def send_event(event_type, event_data):
    to_send = {
        'event': event_type,
        'data': event_data
    }
    urllib2.urlopen(settings.ASYNC_BACKEND_URL, urllib.urlencode(to_send)) 


class Message(models.Model):
    user = models.ForeignKey(User)
    lobby = models.ForeignKey(Lobby)
    action = models.TextField()
    text = models.TextField()
    created_at = models.DateTimeField(u"created at", auto_now_add=True)

    class Meta:
        ordering = ('-id',)

    def __unicode__(self):
        return "%s" % (self.text,)

    def as_dict(self):
        data = {
            'user': self.user.username,
            'action': self.action,
            'text': self.text,
            'players': " ".join(p.username for p in self.lobby.players()),
        }
        return json.dumps(data)

    def save(self, *args, **kwargs):
        print 'saving', self.as_dict()
        super(Message, self).save(*args, **kwargs)
        send_event('message-create', self.as_dict())
