from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Creates read only default superusers for each tenant'

    def handle(self, *args, **options):
        User = get_user_model()
        users = User.objects.all()

        for user in users:
            Token.objects.get_or_create(user=user)
