from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bookings.models import Service, Availability, Booking
from accounts.models import UserProfile
from datetime import datetime, timedelta, time
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Create 30 test bookings for testing purposes'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating 30 test bookings...')

        # Get all providers and customers
        providers = User.objects.filter(userprofile__user_type='provider')
        customers = User.objects.filter(userprofile__user_type='user')

        if not providers.exists():
            self.stdout.write(self.style.ERROR('No providers found! Please create providers first.'))
            return

        if not customers.exists():
            self.stdout.write(self.style.ERROR('No customers found! Please create customers first.'))
            return

        # Get all active services
        services = Service.objects.filter(is_active=True)

        if not services.exists():
            self.stdout.write(self.style.ERROR('No active services found! Please create services first.'))
            return

        # Booking statuses
        statuses = ['pending', 'confirmed', 'completed', 'cancelled']
        status_weights = [0.15, 0.35, 0.40, 0.10]  # 15% pending, 35% confirmed, 40% completed, 10% cancelled

        # Time slots for bookings
        time_slots = [
            (time(9, 0), time(10, 0)),
            (time(10, 30), time(11, 30)),
            (time(12, 0), time(13, 0)),
            (time(14, 0), time(15, 30)),
            (time(16, 0), time(17, 30)),
            (time(18, 0), time(19, 0)),
        ]

        bookings_created = 0

        for i in range(30):
            try:
                # Random service
                service = random.choice(services)
                provider = service.provider
                customer = random.choice(customers)

                # Random date (between 60 days ago and 30 days from now)
                days_offset = random.randint(-60, 30)
                booking_date = datetime.now().date() + timedelta(days=days_offset)

                # Random time slot
                start_time, end_time = random.choice(time_slots)

                # Random status (weighted)
                status = random.choices(statuses, weights=status_weights)[0]

                # Get or create availability for this slot
                availability, created = Availability.objects.get_or_create(
                    provider=provider,
                    service=service,
                    date=booking_date,
                    start_time=start_time,
                    end_time=end_time,
                    defaults={'is_available': False}  # Mark as booked
                )

                # Skip if availability is already booked
                if hasattr(availability, 'booking'):
                    continue

                # Create booking
                booking = Booking.objects.create(
                    customer=customer,
                    provider=provider,
                    service=service,
                    availability=availability,
                    date=booking_date,
                    start_time=start_time,
                    end_time=end_time,
                    price=service.price,
                    status=status,
                    customer_notes=f'Test booking #{i+1}',
                )

                # Mark availability as unavailable
                availability.is_available = False
                availability.save()

                bookings_created += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created booking {bookings_created}/30: {customer.username} → '
                        f'{service.name} ({status}) on {booking_date}'
                    )
                )

            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'Failed to create booking {i+1}: {str(e)}')
                )
                continue

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Successfully created {bookings_created} test bookings!'
            )
        )

        # Show summary statistics
        total_bookings = Booking.objects.count()
        total_revenue = Booking.objects.filter(status='completed').aggregate(
            total=sum('price')
        )

        self.stdout.write('\n📊 Summary:')
        self.stdout.write(f'Total bookings in database: {total_bookings}')
        self.stdout.write(f'Pending: {Booking.objects.filter(status="pending").count()}')
        self.stdout.write(f'Confirmed: {Booking.objects.filter(status="confirmed").count()}')
        self.stdout.write(f'Completed: {Booking.objects.filter(status="completed").count()}')
        self.stdout.write(f'Cancelled: {Booking.objects.filter(status="cancelled").count()}')
