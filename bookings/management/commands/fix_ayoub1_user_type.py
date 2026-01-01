"""
Management command to fix ayoub1 user type issue.
- Reverts ayoub1 back to a regular user (customer)
- Creates a new salon provider account (salon_provider)
- Transfers all salon services and availability to the new provider
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bookings.models import Service, Availability, ProviderProfile
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Fixes ayoub1 user type and transfers salon data to new provider'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Fixing ayoub1 User Type Issue'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

        # Step 1: Get ayoub1 and verify current state
        try:
            ayoub1 = User.objects.get(username='ayoub1')
            self.stdout.write(f'\n✓ Found user: ayoub1')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('✗ User ayoub1 not found!'))
            return

        # Check ayoub1's current user_type
        try:
            ayoub1_profile = UserProfile.objects.get(user=ayoub1)
            current_type = ayoub1_profile.user_type
            self.stdout.write(f'  Current user_type: {current_type}')
        except UserProfile.DoesNotExist:
            self.stdout.write(self.style.WARNING('  No UserProfile found for ayoub1'))
            ayoub1_profile = None
            current_type = None

        # Step 2: Create or get the new salon provider
        self.stdout.write(self.style.SUCCESS('\n--- Creating New Salon Provider ---'))

        salon_provider, created = User.objects.get_or_create(
            username='salon_provider',
            defaults={
                'email': 'salon@test.com',
                'first_name': 'Ayoub',
                'last_name': 'Beauty Salon'
            }
        )

        if created:
            salon_provider.set_password('salonpass123')
            salon_provider.save()
            self.stdout.write(self.style.SUCCESS('✓ Created new provider user: salon_provider'))
        else:
            self.stdout.write(self.style.WARNING('⚠ Provider salon_provider already exists'))

        # Create UserProfile for salon_provider
        salon_user_profile, created = UserProfile.objects.update_or_create(
            user=salon_provider,
            defaults={
                'user_type': 'provider',
                'phone_number': '+31612345678',
                'city': 'Amsterdam',
                'bio': 'Professional beauty salon with comprehensive services',
                'service_type': 'salon_beauty'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created UserProfile for salon_provider'))
        else:
            self.stdout.write(self.style.WARNING('⚠ Updated UserProfile for salon_provider'))

        # Create ProviderProfile for salon_provider
        salon_provider_profile, created = ProviderProfile.objects.update_or_create(
            user=salon_provider,
            defaults={
                'business_name': 'Ayoub Beauty Salon',
                'service_type': 'salon_beauty',
                'bio': 'Professional beauty salon offering premium hair and beauty services',
                'city': 'Amsterdam',
                'phone_number': '+31612345678',
                'years_experience': 8,
                'is_verified': True,
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created ProviderProfile for salon_provider'))
        else:
            self.stdout.write(self.style.WARNING('⚠ Updated ProviderProfile for salon_provider'))

        # Step 3: Transfer services from ayoub1 to salon_provider
        self.stdout.write(self.style.SUCCESS('\n--- Transferring Services ---'))

        services = Service.objects.filter(provider=ayoub1)
        service_count = services.count()

        if service_count > 0:
            services.update(provider=salon_provider)
            self.stdout.write(self.style.SUCCESS(f'✓ Transferred {service_count} services to salon_provider'))
        else:
            self.stdout.write(self.style.WARNING('⚠ No services found for ayoub1'))

        # Step 4: Transfer availability from ayoub1 to salon_provider
        self.stdout.write(self.style.SUCCESS('\n--- Transferring Availability Slots ---'))

        availability_slots = Availability.objects.filter(provider=ayoub1)
        availability_count = availability_slots.count()

        if availability_count > 0:
            availability_slots.update(provider=salon_provider)
            self.stdout.write(self.style.SUCCESS(f'✓ Transferred {availability_count} availability slots to salon_provider'))
        else:
            self.stdout.write(self.style.WARNING('⚠ No availability slots found for ayoub1'))

        # Step 5: Revert ayoub1 back to regular user
        self.stdout.write(self.style.SUCCESS('\n--- Reverting ayoub1 to Regular User ---'))

        if ayoub1_profile:
            # Update user_type back to 'user'
            ayoub1_profile.user_type = 'user'
            ayoub1_profile.service_type = None  # Remove service type
            ayoub1_profile.bio = ''
            ayoub1_profile.save()
            self.stdout.write(self.style.SUCCESS('✓ Reverted ayoub1 UserProfile to user_type="user"'))

        # Delete ProviderProfile for ayoub1 if it exists
        try:
            ayoub1_provider_profile = ProviderProfile.objects.get(user=ayoub1)
            ayoub1_provider_profile.delete()
            self.stdout.write(self.style.SUCCESS('✓ Deleted ProviderProfile for ayoub1'))
        except ProviderProfile.DoesNotExist:
            self.stdout.write(self.style.WARNING('⚠ No ProviderProfile found for ayoub1'))

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS('FIX COMPLETED SUCCESSFULLY'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS(f'✓ ayoub1: Reverted to regular user (customer)'))
        self.stdout.write(self.style.SUCCESS(f'✓ salon_provider: New provider account created'))
        self.stdout.write(self.style.SUCCESS(f'✓ Services transferred: {service_count}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Availability slots transferred: {availability_count}'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('\nLogin credentials for salon_provider:'))
        self.stdout.write(self.style.SUCCESS('  Username: salon_provider'))
        self.stdout.write(self.style.SUCCESS('  Password: salonpass123'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
