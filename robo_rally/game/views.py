from django.views.generic.base import TemplateView
from robo_rally.game.models import Lobby

class LobbiesView(TemplateView):
    template_name = 'courses/maplist.html'
    def get_context_data(self, **kwargs):
        maps = Course.objects.all().values(
            'name', 'length', 'difficulty', 'min_players', 'max_players'
        ).order_by('name')
        return dict(maps=maps)
