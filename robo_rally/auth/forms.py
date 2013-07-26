from django.forms import *
from django.core.validators import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.forms import SetPasswordForm

from robo_rally.auth.models import UserProfile

class Form(Form):
    def __init__(self, request, user, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        self.request = request
        self.user = user

def is_valid_username(username):
    if User.objects.filter(username=username):
        raise ValidationError('The username is already taken')

def is_valid_email(email):
    if User.objects.filter(email=email):
        raise ValidationError('The email is already taken')

def email_exists(email):
    if not User.objects.filter(email=email):
        raise ValidationError("The email does not exist")

def password_field():
    return CharField(
        widget=PasswordInput(),
        max_length=60,
    )

class RegisterForm(Form):
    user = CharField(
        max_length=30,
        validators=[
            RegexValidator(regex=r'^[a-zA-Z0-9]*$',
                message='Username must be Alphanumeric',
                code='invalid_username'
            ),
            is_valid_username
        ]
    )
    email = EmailField(max_length=30, validators=[is_valid_email])
    password = password_field()
    confirm_password = password_field()

    def clean(self):
        data = self.cleaned_data
        same = data.get('password', '') == data.get('confirm_password', '')
        if not same:
            for field in ['password', 'confirm_password']:
                self._errors[field] = self.error_class(['Passwords Must Match'])
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


class ChgPwdForm(Form):
    old_password = password_field()
    new_password = password_field()
    confirm_password = password_field()

    def clean(self):
        data = self.cleaned_data
        same = data.get('new_password', '') == data.get('confirm_password', '')
        if not same:
            for field in ['new_password', 'confirm_password']:
                self._errors[field] = self.error_class(['New Passwords Must Match'])

        old = data.get('old_password', '')
        if not self.user.check_password(old):
            raise ValidationError("Old Password is incorrect")

        return super(ChgPwdForm, self).clean()

    def save(self):
        self.user.set_password(self.cleaned_data['new_password'])
        self.user.save()

class DoResetPwdForm(SetPasswordForm):
    def save(self):
        super(DoResetPwdForm, self).save()

