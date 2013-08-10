from robo_rally.auth.views import FormView
from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseRedirect
from robo_rally.messages.forms import MessageCreateForm

class MessageCreateView(FormView):
    template_name = 'common/blank.html'
    form_class = MessageCreateForm

    def form_valid(self, form):
        self.object = form.save()
        if self.request.is_ajax() and self.object is not None:
            context = {'status': 'ok', 'message': self.object.as_dict()}
            return HttpResponse(json.dumps(context), mimetype="application/json")
        else:
            return HttpResponseRedirect('/')
