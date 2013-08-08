from django.forms import *
from django.conf import settings
from robo_rally.auth.forms import Form
from robo_rally.messages.models import Message

class MessageCreateForm(Form):
    text = CharField()
    action = CharField()

    def save(self):
        action = self.cleaned_data['action']
        if action in settings.VALID_ACTIONS:
            message = Message(
                user=self.user,
                lobby=self.user.get_profile().lobby,
                action=action,
                text=self.cleaned_data['text'],
            )
            message.save()
            return message
        else:
            print 'ACTION %s IS INVALID' % action
