from django.views import generic
from robo_rally.auth.views import FormView
from robo_rally.messages import models
from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseRedirect
from robo_rally.messages.forms import MessageCreateForm

VALID_FUNCTIONS = {

}

class MessageCreateView(FormView):
    form_class = MessageCreateForm
    def form_valid(self, form):
        print form.cleaned_data
        valid = VALID_FUNCTIONS.get(form.cleaned_data['action'], lambda x: True)(form)
        self.object = form.save()
        if self.request.is_ajax() and self.object is not None:
            print self.object.as_dict()
            context = {'status': 'ok', 'message': self.object.as_dict()}
            return HttpResponse(json.dumps(context), mimetype="application/json")
        else:
            return HttpResponseRedirect('/')
