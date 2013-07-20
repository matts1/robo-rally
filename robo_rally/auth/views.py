from robo_rally.auth.forms import RegisterForm
from django.views.generic.edit import FormView

class RegisterView(FormView):
    template_name = 'auth/register.html'
    form_class = RegisterForm
    success_url = '/register' #TODO: should be /, but first get this working

    def form_valid(self, form):
        form.save()
        return super(RegisterView, self).form_valid(form)
