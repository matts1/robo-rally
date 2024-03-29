from django.contrib.sessions.models import Session
from robo_rally.auth.forms import *
from django.views.generic.edit import FormView
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.signals import user_logged_out, user_logged_in

class FormView(FormView):
    extra_args = True
    def get_form_kwargs(self):
        kwargs = super(FormView, self).get_form_kwargs()
        for key, val in self.kwargs.items():
            kwargs[key] = val

        if self.extra_args:
            kwargs['request'] = self.request
            kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        if hasattr(self, 'success_message'):
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
    form_class = PasswordResetForm
    extra_args = False
    success_url = reverse_lazy('login')
    success_message = 'An email has been sent with instructions on how to reset your password'

class MsgView(RedirectView):
    messages = {
        'doreset': 'Your password has been reset. You may now log in'
    }
    def get_redirect_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, self.messages[kwargs['msg']])
        return reverse_lazy(kwargs['redirect'])

def logout(user, **kwargs):
    profile = user.get_profile()
    profile.leave_lobby()
    profile.session = None
    profile.save()

def login(sender, user, request, **kwargs):
    # the session still has not been created for the new user at this stage
    for session in Session.objects.all():
        if session.get_decoded().get('_auth_user_id') == user.id:
            session.delete()

user_logged_out.connect(logout)
user_logged_in.connect(login)
