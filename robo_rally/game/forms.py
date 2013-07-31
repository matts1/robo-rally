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
        lobby = Lobby(self.cleaned_data['name'], datetime.now())
        lobby.save()
        lobbyperson = LobbyPerson(self.user, lobby, 0, datetime.now())
        lobbyperson.save()