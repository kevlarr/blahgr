"""
Queries to support the blog views
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .models import Post


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


def headline_post() -> Post:
    """
    Returns the latest post
    """
    return Post.objects.prefetch_related('author').first()


def post_summaries(*, offset: int = 0) -> list[PostSummary]:
    """
    Returns high-level details for every post starting at the given offset
    """
    if offset < 0:
        raise OffsetError(offset)

    queryset = (Post
        .objects
        .values_list('id', 'title', 'created_at', 'author__username')
        .all()
        [offset:])

    return [PostSummary(
        id=row[0],
        title=row[1],
        created_at=row[2],
        author_username=row[3],
    ) for row in queryset]


