"""
Forms supporting blog views
"""
from django import forms

from .models import Comment, Post


class CommentForm(forms.ModelForm):
    """
    Form to create a new comment
    """
    class Meta:
        model = Comment
        fields = ['text']


class PostForm(forms.ModelForm):
    """
    Form to create a new post
    """
    class Meta:
        model = Post
        fields = ['title', 'text']
