from django.forms import *
from django.core.validators import *
from django.contrib.auth.models import User

from robo_rally.auth.models import UserProfile

def is_valid_username(username):
    return #TODO: after users are working, get this working

def is_valid_email(email):
    return #TODO: after users are working, get this working

class RegisterForm(Form):
    user = CharField(
        max_length=30,
        validators=[
            RegexValidator(regex=r'^[a-zA-Z0-9]*$',
                message='Username must be Alphanumeric',
            ),
            is_valid_username
        ]
    )
    email = EmailField(max_length=30)
    password = CharField(
        widget=PasswordInput(),
        max_length=60
    )
    confirm_password = CharField(
        widget=PasswordInput(),
        max_length=60,
    )

    def clean(self):
        data = self.cleaned_data
        same = data.get('password', '') == data.get('confirm_password', '')
        if not same:
            for field in ['password', 'confirm_password']:
                self._errors[field] = self.error_class(['Passwords must Match'])
        return super(RegisterForm, self).clean()

    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(
            data['user'],
            data['email'],
            data['password']
        )
        profile = UserProfile(
            user=user,
            activation_key=None,
        )
        user.save()
        return user
