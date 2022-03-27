"""
Queries to support the blog views
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from django.db.models import Prefetch

from .models import Comment, Post


class OffsetError(Exception):
    def __init__(self, offset):
        self.message = f'Offset must be a whole number, received {offset}'


@dataclass
class PostSummary:
    """
    High-level summary of the post
    """
    author_username: str
    created_at: datetime
    id: int
    title: str


def post(post_id: int) -> Post:
    """
    Returns the post by id along with author and comments ordered chronologically
    """
    comments = Prefetch(
        'comments',
        queryset=Comment.objects
            .prefetch_related('author')
            .order_by('created_at'),
    )
    return (Post.objects
        .prefetch_related('author', comments)
        .get(pk=post_id))


def headline_post() -> Post:
    """
    Returns the latest post with author preloaded
    """
    return (Post.objects
        .prefetch_related('author')
        .order_by('-created_at')
        .first())


def post_summaries(*, offset: int = 0) -> list[PostSummary]:
    """
    Returns high-level details for every post starting at the given offset
    """
    if offset < 0:
        raise OffsetError(offset)

    queryset = (Post
        .objects
        .values_list('id', 'title', 'created_at', 'author__username')
        .order_by('-created_at')
        .all()
        [offset:])

    return [PostSummary(
        id=row[0],
        title=row[1],
        created_at=row[2],
        author_username=row[3],
    ) for row in queryset]


def comment(comment_id: int) -> Comment:
    """
    Returns the comment by id along with author
    """
    return (Comment.objects
        .prefetch_related('author')
        .get(pk=comment_id))
