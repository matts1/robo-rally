from django.contrib.auth.models import AnonymousUser
from django.forms import *
from django.conf import settings
from robo_rally.auth.forms import Form
from robo_rally.courses.models import Course
from robo_rally.game.models import *
from robo_rally.messages.models import Message

def pick_map(action, text, user):
    if user.get_profile().index != 0:
        raise ValidationError('The lobby leader needs to be the one to do that')
    if user.get_profile().lobby.game_stage != LOBBY:
        raise ValidationError("The game has already been started")

    user.get_profile().lobby.goto_pickmap()
    return False

def start_game(action, course, user):
    if user.get_profile().index != 0:
        raise ValidationError('The lobby leader needs to be the one to do that')
    if not Course.objects.filter(filename=course):
        raise ValidationError('Invalid course filename')
    lobby = user.get_profile().lobby
    if lobby.game_stage == IN_GAME:
        raise ValidationError('Game is already started')
    lobby.start_game(course)

def getleader(action, text, user):
    lobby = user.get_profile.lobby
    print lobby.leader()

def player_confirmed(action, text, user):
    user.get_profile().get_game_player().ready()
    
def swapcards(action, text, user):
    c1, c2 = map(int, text.split(' '))
    user.get_profile().get_game_player().swapcards(c1, c2)

def power_down(action, text, user):
    player = user.get_profile().get_game_player()
    if player.power_down != 0:
        player.power_down = 1

def set_option(action, text, user):
    if text == 'recompile':
        user.get_profile().get_game_player().recompile()

PERFORM_FUNCTIONS = {
    'gotopickmap': pick_map,
    'adduser': getleader,
    'deleteuser': getleader,
    'startgame': start_game,
    'swapcards': swapcards,
    'playerready': player_confirmed,
    'powerdown': power_down,
    'setoption': set_option,
}

class MessageCreateForm(Form):
    text = CharField(required=False)
    action = CharField()

    def clean(self):
        if isinstance(self.user, AnonymousUser):
            raise ValidationError('Player is not logged in')
        if self.user.get_profile().lobby is None:
            raise ValidationError('Player not in lobby')
        self.user.get_profile().ping()
        self.user.get_profile().lobby.remove_old_players()
        data = self.cleaned_data
        if data['action'] != 'ping':
            print 'Received message', data
        valid_fn = PERFORM_FUNCTIONS.get(data['action'], lambda *x: True)
        # raise ValidationError if it isn't valid
        try:
            res = valid_fn(data['action'], data['text'], self.user)
        except ValidationError as e:
            print 'Invalid:', e
            raise e
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
