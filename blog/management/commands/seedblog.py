"""
Exposes a command to generate test data for the blog models,
as well as a handful of authors

See: https://docs.djangoproject.com/en/4.0/howto/custom-management-commands/
"""
from django.contrib import auth
from django.core.management.base import BaseCommand
from django_seed import Seed

from blog.models import Post, Comment


USER = auth.get_user_model()


class Command(BaseCommand):
    """
    Blog model seeder command
    """

    help = 'Seeds the blog with sample data'

    def __init__(self):
        self.seeder = Seed.seeder()

    def handle(self, *args, **options):
        """
        Seeds users, posts, and comments such that:
            - Some users SHOULD have multiple posts and comments
            - Some posts SHOULD have multiple comments
        """
        self.seeder.add_entity(USER, 5)
        self.seeder.add_entity(Post, 15, {
            'text': lambda _: self.seeder.faker.paragraph(10),
        })
        self.seeder.add_entity(Comment, 45, {
            'text': lambda _: self.seeder.faker.paragraph(3),
        })
        self.seeder.execute()
