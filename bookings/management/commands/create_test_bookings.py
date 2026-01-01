"""
Management command to create comprehensive test data for the booking system.
This creates 25+ availability slots and bookings to test the system thoroughly.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bookings.models import Service, Availability, Booking, ProviderProfile
from accounts.models import UserProfile
from datetime import datetime, timedelta, time
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Creates comprehensive test data with 25+ availability slots and bookings'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Creating Comprehensive Test Data'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

        # Get or create provider
        provider_user = self.get_or_create_provider()

        # Get or create services
        services = self.create_services(provider_user)

        # Get or create customer
        customer_user = self.get_or_create_customer()

        # Create availability slots (25+ slots)
        availability_slots = self.create_availability_slots(provider_user, services)

        # Create bookings (mix of booked and available slots)
        bookings = self.create_bookings(customer_user, provider_user, services, availability_slots)

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS('TEST DATA CREATED SUCCESSFULLY'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS(f'✓ Provider: {provider_user.username}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Services: {len(services)}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Availability Slots: {len(availability_slots)}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Bookings Created: {len(bookings)}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Available Slots: {len(availability_slots) - len(bookings)}'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

    def get_or_create_provider(self):
        """Get or create test provider user"""
        username = 'test_provider'

        try:
            provider_user = User.objects.get(username=username)
            self.stdout.write(self.style.WARNING(f'Using existing provider: {username}'))
        except User.DoesNotExist:
            provider_user = User.objects.create_user(
                username=username,
                email='testprovider@test.com',
                password='testpass123',
                first_name='Test',
                last_name='Provider'
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Created provider user: {username}'))

        # Create or get UserProfile (required for dashboard to show provider stats)
        try:
            user_profile = UserProfile.objects.get(user=provider_user)
            self.stdout.write(self.style.WARNING(f'UserProfile already exists'))
        except UserProfile.DoesNotExist:
            user_profile = UserProfile.objects.create(
                user=provider_user,
                user_type='provider',
                phone_number='+31612345678',
                city='Amsterdam',
                bio='Professional test salon for comprehensive booking system testing',
                service_type='salon_beauty'
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Created UserProfile (user_type=provider)'))

        # Create or get provider profile
        try:
            profile = ProviderProfile.objects.get(user=provider_user)
            self.stdout.write(self.style.WARNING(f'ProviderProfile already exists'))
        except ProviderProfile.DoesNotExist:
            profile = ProviderProfile.objects.create(
                user=provider_user,
                business_name='Test Beauty Salon',
                service_type='salon_beauty',
                bio='Professional test salon for comprehensive booking system testing',
                city='Amsterdam',
                phone_number='+31612345678',
                years_experience=10,
                is_verified=True,
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Created ProviderProfile'))

        return provider_user

    def get_or_create_customer(self):
        """Get or create test customer user"""
        username = 'test_customer'

        try:
            customer_user = User.objects.get(username=username)
            self.stdout.write(self.style.WARNING(f'Using existing customer: {username}'))
        except User.DoesNotExist:
            customer_user = User.objects.create_user(
                username=username,
                email='testcustomer@test.com',
                password='testpass123',
                first_name='Test',
                last_name='Customer'
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Created customer user: {username}'))

        return customer_user

    def create_services(self, provider_user):
        """Create multiple services for testing"""
        services_data = [
            {
                'name': 'Haircut',
                'category': 'salon_beauty',
                'description': 'Professional haircut service',
                'price': Decimal('35.00'),
                'duration': 60  # 1 hour
            },
            {
                'name': 'Hair Coloring',
                'category': 'salon_beauty',
                'description': 'Full hair coloring service',
                'price': Decimal('80.00'),
                'duration': 120  # 2 hours
            },
            {
                'name': 'Quick Trim',
                'category': 'salon_beauty',
                'description': 'Quick hair trim',
                'price': Decimal('20.00'),
                'duration': 30  # 30 minutes
            },
        ]

        services = []
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                provider=provider_user,
                name=service_data['name'],
                defaults=service_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created service: {service.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Using existing service: {service.name}'))
            services.append(service)

        return services

    def create_availability_slots(self, provider_user, services):
        """Create 25+ availability slots across multiple days"""
        slots = []
        today = datetime.now().date()

        # Time slots for each day
        time_slots = [
            (time(9, 0), time(10, 0)),
            (time(10, 0), time(11, 0)),
            (time(11, 0), time(12, 0)),
            (time(13, 0), time(14, 0)),
            (time(14, 0), time(15, 0)),
            (time(15, 0), time(16, 0)),
            (time(16, 0), time(17, 0)),
        ]

        self.stdout.write(self.style.SUCCESS('\nCreating availability slots...'))

        # Create slots for next 5 days (5 days × 7 slots = 35 slots)
        for day_offset in range(1, 6):
            current_date = today + timedelta(days=day_offset)

            for start_time, end_time in time_slots:
                # Randomly assign to different services
                service = random.choice(services)

                # Check if slot already exists
                existing = Availability.objects.filter(
                    provider=provider_user,
                    service=service,
                    date=current_date,
                    start_time=start_time,
                    end_time=end_time
                ).first()

                if not existing:
                    slot = Availability.objects.create(
                        provider=provider_user,
                        service=service,
                        date=current_date,
                        start_time=start_time,
                        end_time=end_time,
                        is_available=True
                    )
                    slots.append(slot)
                    self.stdout.write(
                        f'  • {current_date} {start_time}-{end_time} - {service.name}'
                    )
                else:
                    slots.append(existing)
                    self.stdout.write(
                        self.style.WARNING(
                            f'  ⚠ Slot already exists: {current_date} {start_time}-{end_time}'
                        )
                    )

        self.stdout.write(self.style.SUCCESS(f'\n✓ Total availability slots: {len(slots)}'))
        return slots

    def create_bookings(self, customer_user, provider_user, services, availability_slots):
        """Create bookings for some of the availability slots"""
        bookings = []

        # Book approximately 40% of available slots
        num_bookings = min(15, int(len(availability_slots) * 0.4))

        self.stdout.write(self.style.SUCCESS(f'\nCreating {num_bookings} bookings...'))

        # Randomly select slots to book
        slots_to_book = random.sample(availability_slots, num_bookings)

        for slot in slots_to_book:
            # Check if already booked
            if not slot.is_available:
                self.stdout.write(
                    self.style.WARNING(f'  ⚠ Slot already booked: {slot.date} {slot.start_time}')
                )
                continue

            # Check if booking already exists for this slot
            existing_booking = Booking.objects.filter(availability=slot).first()
            if existing_booking:
                self.stdout.write(
                    self.style.WARNING(f'  ⚠ Booking already exists: {slot.date} {slot.start_time}')
                )
                bookings.append(existing_booking)
                continue

            # Create booking
            booking = Booking.objects.create(
                customer=customer_user,
                provider=provider_user,
                service=slot.service,
                availability=slot,
                date=slot.date,
                start_time=slot.start_time,
                end_time=slot.end_time,
                price=slot.service.price,
                status=random.choice(['pending', 'confirmed', 'confirmed', 'confirmed'])  # Mostly confirmed
            )

            # Mark slot as unavailable
            slot.is_available = False
            slot.save()

            bookings.append(booking)
            self.stdout.write(
                f'  • Booked: {slot.date} {slot.start_time}-{slot.end_time} - {slot.service.name} ({booking.status})'
            )

        self.stdout.write(self.style.SUCCESS(f'\n✓ Created {len(bookings)} bookings'))
        return bookings
