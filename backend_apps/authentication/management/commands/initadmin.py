from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from backend_apps.users.models import RoleChoices

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates a default superuser if none exists'

    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role=RoleChoices.SYSTEM_ADMINISTRATOR,
            )
            self.stdout.write(self.style.SUCCESS('Default superuser created:'))
            self.stdout.write('  Username: admin')
            self.stdout.write('  Password: admin123')
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists, skipping creation'))
