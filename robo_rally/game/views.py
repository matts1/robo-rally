from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView
from robo_rally.auth.views import FormView
from robo_rally.game.forms import CreateLobbyForm
from robo_rally.game.models import *

class LobbiesView(TemplateView):
    template_name = 'courses/lobbies.html'
    def get_context_data(self, **kwargs):
        lobbies = Lobby.objects.all()
        return dict(lobbies=lobbies)

class CreateLobbyView(FormView):
    template_name = 'courses/createlobby.html'
    form_class = CreateLobbyForm
    success_url = reverse_lazy('lobbies')
    success_message = 'Lobby created successfully!'