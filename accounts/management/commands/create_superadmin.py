from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Create a superadmin user for the booking system'

    def handle(self, *args, **kwargs):
        username = 'superadmin'
        email = 'admin@example.com'
        password = 'admin123'

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Superadmin user "{username}" already exists!'))
            return

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Super',
            last_name='Admin'
        )

        # Create the user profile with superadmin type
        UserProfile.objects.create(
            user=user,
            user_type='superadmin',
            phone_number='+31 6 12345678'
        )

        self.stdout.write(self.style.SUCCESS('✓ Successfully created superadmin user!'))
        self.stdout.write(self.style.SUCCESS(f'\nLogin credentials:'))
        self.stdout.write(self.style.SUCCESS(f'  Username: {username}'))
        self.stdout.write(self.style.SUCCESS(f'  Password: {password}'))
        self.stdout.write(self.style.SUCCESS(f'  Email: {email}'))
        self.stdout.write(self.style.WARNING(f'\n⚠ Please change the password after first login!'))
