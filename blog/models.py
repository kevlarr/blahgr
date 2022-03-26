# from django.contrib.auth.models import User
from django.contrib import auth
from django.db import models

class Post(models.Model):
    """
    A blog post
    """

    class Meta:
        ordering = ['-created_at']

    author = models.ForeignKey(
        auth.get_user_model(),
        null=False,
        on_delete=models.RESTRICT,
    )
    title = models.TextField(
        null=False,
        help_text='The title of the blog post',
    )
    text = models.TextField(
        null=False,
        help_text='The contents of the blog post',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Comment(models.Model):
    """
    A comment on a blog post
    """

    class Meta:
        ordering = ['-created_at']

    author = models.ForeignKey(
        auth.get_user_model(),
        null=False,
        on_delete=models.RESTRICT,
    )
    post = models.ForeignKey(
        'Post',
        null=False,
        on_delete=models.RESTRICT,
    )
    text = models.TextField(
        null=False,
        help_text='The contents of the comment',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
