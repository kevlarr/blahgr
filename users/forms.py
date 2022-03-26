"""
Forms supporting users views
"""
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class SignupForm(UserCreationForm):
    """
    Form to create a new user with username & password
    """


class LoginForm(AuthenticationForm):
    """
    Form to allow an existing user to log in with username & password
    """
