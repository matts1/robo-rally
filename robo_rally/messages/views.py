from django.views import generic
from robo_rally.auth.views import FormView
from robo_rally.messages import models
from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from robo_rally.messages.forms import MessageCreateForm


class MessageListView(generic.ListView):
    queryset = models.Message.objects.all()[:10]

    def get_context_data(self, *args, **kwargs):
        context = super(MessageListView, self).get_context_data(*args, **kwargs)
        context['async_url'] = settings.ASYNC_BACKEND_URL
        return context

class MessageCreateView(FormView):
    form_class = MessageCreateForm
    def form_valid(self, form):
        self.object = form.save()
        if self.request.is_ajax() and self.object is not None:
            print self.object.as_dict()
            context = {'status': 'ok', 'message': self.object.as_dict()}
            return HttpResponse(json.dumps(context), mimetype="application/json")
        else:
            return HttpResponseRedirect('/')
