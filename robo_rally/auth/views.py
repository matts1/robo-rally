from robo_rally.auth.forms import *
from django.views.generic.edit import FormView

class RegisterView(FormView):
    template_name = 'auth/register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super(RegisterView, self).form_valid(form)

class ChgPwdView(FormView):
    template_name = 'auth/chgpwd.html'
    form_class = ChgPwdForm
    success_url='/chgpwd'

    def form_valid(self, form):
        form.save()
        return super(ChgPwdView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ChgPwdView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
