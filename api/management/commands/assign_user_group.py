from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('--group', type=str, default='backoffice')

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username=options['username'])
            group, created = Group.objects.get_or_create(name=options['group'])
            user.groups.add(group)
            self.stdout.write(f"Added {user.username} to {group.name} group")
        except User.DoesNotExist:
            self.stdout.write("User not found")