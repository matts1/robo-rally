from datetime import datetime

from robo_rally.auth.forms import *
from robo_rally.game.models import *

class CreateLobbyForm(Form):
    name = CharField(
        max_length=30,
        validators=[
            RegexValidator(regex=r'^[a-zA-Z0-9]*$',
                message='Lobby name must be alphanumeric',
                code='invalid_lobby_name'
            ),
        ]
    )

    def save(self):
        lobby = Lobby(self.cleaned_data['name'])
        lobby.save()
        profile = self.user.get_profile()
        profile.lobby = lobby
        profile.index = 0
        profile.last_ping = datetime.now()
        profile.save()
