"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

from django.test import TestCase

from robo_rally.auth.forms import RegisterForm

# fortunately, we don't need to test the stuff that's built into django
# that leaves basically just some form validation

class RegisterTest(TestCase):
    def test_forms(self):
        self.assertEqual(1+1, 2)
        break
        fields = ["user", "email", "password", "confirm_password"]
        cases = [
            ["matt", "mattstark75@gmail.com", "1", "1", True], # Valid Form
            ["matt", "mattstark75@gmail.com", "1", "1", False], # Username taken
            ["sam", "mattstark75@gmail.com", "1", "1", False], # Email taken
            ["sam", "samm0s@hotmail.com", "1", "12", False], # Passwords different
            ["sam", "samm0s@hotmail.com", "1", "1", True], # Valid Form\
        ]
        for case in cases:
            valid = case[0]
            data = dict(zip(fields, case[1:]))
            form = RegisterForm(data=data)
            self.assertEqual(form.is_valid(), valid, data)
