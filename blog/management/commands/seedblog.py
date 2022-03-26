from django.contrib import auth
from django.core.management.base import BaseCommand
from django_seed import Seed

from blog.models import Post, Comment


USER = auth.get_user_model()


class Command(BaseCommand):
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
        self.seeder.add_entity(Post, 15)
        self.seeder.add_entity(Comment, 45)
        self.seeder.execute()
