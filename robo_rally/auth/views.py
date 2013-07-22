from robo_rally.auth.forms import *
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm

class FormView(FormView):
    def get_form_kwargs(self):
        kwargs = super(FormView, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        print "checking for message"
        if hasattr(self, 'success_message'):
            print "adding message"
            messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return super(FormView, self).form_valid(form)

class RegisterView(FormView):
    template_name = 'auth/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    success_message = 'Your account has been created. You may now log in'

class ChgPwdView(FormView):
    template_name = 'auth/chgpwd.html'
    form_class = ChgPwdForm
    success_url = reverse_lazy('chgpwd')
    success_message = 'Your Password Has Been Changed'

class ResetPwdView(FormView):
    template_name = 'auth/resetpwd.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('login')
    # TODO: this does not have a message
    # TODO: check that the reset itself is working (url resetpwd/reset/code)
    success_message = 'An email has been sent with instructions on how to reset your password'
