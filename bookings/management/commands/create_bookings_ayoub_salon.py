"""
Management command to create 200 days of availability for ayoub1 salon provider
with multiple salon services.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bookings.models import Service, Availability, ProviderProfile
from accounts.models import UserProfile
from datetime import datetime, timedelta, time
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Creates 200 days of availability for ayoub1 with salon services'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Creating Ayoub1 Salon Test Data'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

        # Get or verify ayoub1 user
        try:
            provider_user = User.objects.get(username='ayoub1')
            self.stdout.write(self.style.SUCCESS(f'✓ Found provider: {provider_user.username}'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('✗ User ayoub1 not found!'))
            return

        # Update or create UserProfile
        user_profile, created = UserProfile.objects.update_or_create(
            user=provider_user,
            defaults={
                'user_type': 'provider',
                'phone_number': '+31612345678',
                'city': 'Amsterdam',
                'bio': 'Professional beauty salon with comprehensive services',
                'service_type': 'salon_beauty'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created UserProfile'))
        else:
            self.stdout.write(self.style.WARNING('⚠ Updated existing UserProfile'))

        # Create or update ProviderProfile
        provider_profile, created = ProviderProfile.objects.update_or_create(
            user=provider_user,
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
            self.stdout.write(self.style.SUCCESS('✓ Created ProviderProfile'))
        else:
            self.stdout.write(self.style.WARNING('⚠ Updated existing ProviderProfile'))

        # Create salon services
        services = self.create_services(provider_user)

        # Create 200 days of availability
        availability_count = self.create_availability(provider_user, services, days=200)

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS('TEST DATA CREATED SUCCESSFULLY'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS(f'✓ Provider: {provider_user.username}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Services: {len(services)}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Total Availability Slots: {availability_count}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Date Range: {datetime.now().date()} to {(datetime.now() + timedelta(days=200)).date()}'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

    def create_services(self, provider_user):
        """Create salon services"""
        services_data = [
            {
                'name': 'Quick Trim',
                'category': 'salon_beauty',
                'description': 'Fast and professional hair trim',
                'price': Decimal('20.00'),
                'duration': 30  # 30 minutes
            },
            {
                'name': 'Haircut & Styling',
                'category': 'salon_beauty',
                'description': 'Complete haircut with professional styling',
                'price': Decimal('45.00'),
                'duration': 60  # 1 hour
            },
            {
                'name': 'Hair Coloring',
                'category': 'salon_beauty',
                'description': 'Professional hair coloring service',
                'price': Decimal('95.00'),
                'duration': 120  # 2 hours
            },
            {
                'name': 'Highlights & Lowlights',
                'category': 'salon_beauty',
                'description': 'Professional hair highlighting service',
                'price': Decimal('110.00'),
                'duration': 150  # 2.5 hours
            },
            {
                'name': 'Deep Conditioning Treatment',
                'category': 'salon_beauty',
                'description': 'Intensive hair treatment and conditioning',
                'price': Decimal('55.00'),
                'duration': 45  # 45 minutes
            },
            {
                'name': 'Blowout & Style',
                'category': 'salon_beauty',
                'description': 'Professional blow dry and styling',
                'price': Decimal('35.00'),
                'duration': 45  # 45 minutes
            },
            {
                'name': 'Keratin Treatment',
                'category': 'salon_beauty',
                'description': 'Full keratin smoothing treatment',
                'price': Decimal('180.00'),
                'duration': 180  # 3 hours
            },
        ]

        services = []
        for service_data in services_data:
            service, created = Service.objects.update_or_create(
                provider=provider_user,
                name=service_data['name'],
                defaults=service_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created service: {service.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Updated service: {service.name}'))
            services.append(service)

        return services

    def create_availability(self, provider_user, services, days=200):
        """Create availability for 200 days"""
        self.stdout.write(self.style.SUCCESS(f'\nCreating availability for {days} days...'))

        today = datetime.now().date()
        total_slots = 0

        # Time slots for weekdays (Monday-Friday)
        weekday_slots = [
            (time(9, 0), time(12, 0)),   # Morning: 9 AM - 12 PM
            (time(13, 0), time(17, 0)),  # Afternoon: 1 PM - 5 PM
            (time(17, 0), time(20, 0)),  # Evening: 5 PM - 8 PM
        ]

        # Time slots for weekends (Saturday-Sunday)
        weekend_slots = [
            (time(10, 0), time(14, 0)),  # Morning: 10 AM - 2 PM
            (time(14, 0), time(18, 0)),  # Afternoon: 2 PM - 6 PM
        ]

        for day_offset in range(days):
            current_date = today + timedelta(days=day_offset)
            is_weekend = current_date.weekday() >= 5  # Saturday=5, Sunday=6

            # Choose time slots based on day of week
            time_slots = weekend_slots if is_weekend else weekday_slots

            # For each time slot
            for start_time, end_time in time_slots:
                # Randomly select 2-4 services for this time slot
                num_services = random.randint(2, min(4, len(services)))
                selected_services = random.sample(services, num_services)

                for service in selected_services:
                    # Calculate how many slots to create based on service duration
                    current_slot_start = start_time

                    while True:
                        # Calculate end time for this slot
                        start_datetime = datetime.combine(current_date, current_slot_start)
                        slot_end_datetime = start_datetime + timedelta(minutes=service.duration)
                        current_slot_end = slot_end_datetime.time()

                        # Check if this slot goes beyond the end time
                        end_datetime = datetime.combine(current_date, end_time)
                        if slot_end_datetime > end_datetime:
                            break

                        # Check if slot already exists
                        exists = Availability.objects.filter(
                            provider=provider_user,
                            service=service,
                            date=current_date,
                            start_time=current_slot_start,
                            end_time=current_slot_end
                        ).exists()

                        if not exists:
                            Availability.objects.create(
                                provider=provider_user,
                                service=service,
                                date=current_date,
                                start_time=current_slot_start,
                                end_time=current_slot_end,
                                is_available=True
                            )
                            total_slots += 1

                        # Move to next slot
                        current_slot_start = current_slot_end

            # Progress indicator every 20 days
            if (day_offset + 1) % 20 == 0:
                self.stdout.write(f'  Progress: {day_offset + 1}/{days} days completed ({total_slots} slots created so far)')

        self.stdout.write(self.style.SUCCESS(f'\n✓ Created {total_slots} availability slots across {days} days'))
        return total_slots
