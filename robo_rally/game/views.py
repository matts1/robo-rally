from django.core.urlresolvers import reverse_lazy
from robo_rally.auth.views import FormView
from robo_rally.game.forms import CreateLobbyForm
from robo_rally.game.models import *

class LobbiesView(FormView):
    template_name = 'courses/lobbies.html'
    form_class = CreateLobbyForm
    success_url = reverse_lazy('lobbies')
    success_message = 'Lobby created successfully!'
    def get_context_data(self, **kwargs):
        lobbies = super(LobbiesView, self).get_context_data(**kwargs)
        lobbies.update(lobbies=Lobby.objects.all())
        return lobbies
