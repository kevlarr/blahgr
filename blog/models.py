"""
Blog models
"""
from django.contrib import auth
from django.db import models
from django.utils.timezone import now


class BaseModel(models.Model):
    """
    Base model to include columns common across all tables
    """
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SoftDeletableQuerySet(models.query.QuerySet):
    """
    Custom query set to enable bulk soft-deletion
    """
    def delete(self):
        """
        Marks all matching records as soft-deleted
        """
        self.update(deleted_at=now())


class SoftDeletableManager(models.Manager):
    """
    Custom manager to return only non-deleted objects
    """
    def get_queryset(self):
        """
        Returns a query set that selects only non-deleted objects
        and overrides default bulk deletion
        """
        return (SoftDeletableQuerySet(self.model)
            .filter(deleted_at=None))


class SoftDeletable(BaseModel):
    """
    Base model class to support soft deletes, either on the individual record
    or in bulk using a query set
    """
    class Meta:
        abstract = True

    deleted_at = models.DateTimeField(null=True)

    objects = SoftDeletableManager()

    def delete(self):
        """
        Marks a record as deleted
        """
        self.deleted_at = now()
        self.save()


class Post(SoftDeletable):
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


class Comment(SoftDeletable):
    """
    A comment on a blog post
    """
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
