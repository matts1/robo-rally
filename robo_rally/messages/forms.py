from django.forms import *
from django.conf import settings
from robo_rally.auth.forms import Form
from robo_rally.game.models import LOBBY
from robo_rally.messages.models import Message

def pick_map(action, text, user):
    if user.get_profile().index != 0:
        raise ValidationError('The lobby leader needs to be the one to do that')
    if user.get_profile().lobby.size() < 2:
        raise ValidationError('You can\'t start a lobby with only one person')
    if user.get_profile().lobby.game_stage != LOBBY:
        raise ValidationError("The game has already been started")

    user.get_profile().lobby.goto_pickmap()
    return False

def getleader(action, text, user):
    lobby = user.get_profile.lobby
    print lobby.leader()


PERFORM_FUNCTIONS = {
    'goto_pickmap': pick_map,
    'adduser': getleader,
    'deleteuser': getleader,
}

class MessageCreateForm(Form):
    text = CharField(required=False)
    action = CharField()

    def clean(self):
        self.user.get_profile().ping()
        self.user.get_profile().lobby.remove_old_players()
        data = self.cleaned_data
        print data
        valid_fn = PERFORM_FUNCTIONS.get(data['action'], lambda *x: True)
        # raise ValidationError if it isn't valid
        res = valid_fn(data['action'], data['text'], self.user)
        if res == False:
            raise ValidationError('Not an error, but don\'t want form to go through')
        elif res is not None:
            self.cleaned_data['text'] = res
        return super(MessageCreateForm, self).clean()

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
