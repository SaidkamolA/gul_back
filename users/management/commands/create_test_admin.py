from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Creates a test admin user'

    def handle(self, *args, **options):
        username = 's'
        password = '1'
        email = 'admin@example.com'

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_admin=True,
                is_email_verified=True
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created admin user: {username}'))
        else:
            self.stdout.write(self.style.WARNING(f'User {username} already exists')) 