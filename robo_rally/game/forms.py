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
        name = self.cleaned_data['name'].strip().title()
        self.lobby = Lobby.objects.filter(name=name)
        if not self.lobby:
            self.lobby = Lobby(name)
            self.lobby.save()
        else:
            self.lobby = self.lobby[0]
        self.lobby.add_user(self.user)
