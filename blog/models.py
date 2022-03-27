"""
Blog models
"""
from django.contrib import auth
from django.db import models


class Post(models.Model):
    """
    A blog post
    """
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author_id', 'title'],
                name='blog_post_author_id_title_uniq',
            ),
        ]
        ordering = ['-created_at']

    author = models.ForeignKey(
        auth.get_user_model(),
        null=False,
        on_delete=models.RESTRICT,
    )
    title = models.CharField(
        # Quick googlefu indicates 'ideal' title lengths around 50-60 characters,
        # which also helps keep titles more 'sluggable' for URLs
        max_length=100,
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
        related_name='comments',
    )
    text = models.TextField(
        null=False,
        help_text='The contents of the comment',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
