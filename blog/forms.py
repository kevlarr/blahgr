"""
Forms supporting blog views
"""
from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """
    Form to create a new user with username & password
    """
    class Meta:
        model = Post
        fields = ['title', 'text']
