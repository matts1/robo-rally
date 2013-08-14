from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.base import RedirectView, TemplateView

from robo_rally.auth.views import FormView
from robo_rally.game.forms import CreateLobbyForm
from robo_rally.game.models import *


class LobbiesView(FormView):
    template_name = 'courses/lobbies.html'
    form_class = CreateLobbyForm
    success_url = reverse_lazy('currentlobby')
    success_message = 'Lobby created successfully!'
    def get_context_data(self, **kwargs):
        Lobby.remove_empty_lobbies()
        lobbies = super(LobbiesView, self).get_context_data(**kwargs)
        lobbies.update(lobbies=Lobby.objects.filter(game_stage=LOBBY))
        return lobbies

class JoinLobbyView(RedirectView):
    permanent = False
    url = reverse_lazy('currentlobby')
    def get(self, request, *args, **kwargs):
        self.user = request.user
        return super(JoinLobbyView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, lobby, **kwargs):
        Lobby.objects.filter(name=lobby)[0].add_user(self.user)
        return super(JoinLobbyView, self).get_redirect_url(**kwargs)

class CurrentLobbyView(TemplateView):
    template_name = 'courses/viewlobby.html'
    def get(self, request, *args, **kwargs):
        self.profile = request.user.get_profile()
        if self.profile.lobby is None:
            return HttpResponseRedirect(reverse_lazy('lobbies'))
        else:
            return super(CurrentLobbyView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CurrentLobbyView, self).get_context_data(**kwargs)
        self.profile.ping()
        context.update(lobby=self.profile.lobby)
        context.update(async_url=settings.ASYNC_BACKEND_URL)
        return context

class GameView(TemplateView):
    template_name = 'game/gameview.html'
    def get(self, request, *args, **kwargs):
        self.user = request.user
        self.profile = request.user.get_profile()
        if self.profile.lobby is None or self.profile.lobby.get_game() is None:
            return HttpResponseRedirect('/')
        else:
            return super(GameView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GameView, self).get_context_data(**kwargs)
        self.profile.ping()
        context.update(
            game=self.profile.lobby.get_game(),
            player=self.profile.get_game_player(),
        )
        return context
