from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bookings.models import Service, Availability
from datetime import datetime, timedelta, time
import random


class Command(BaseCommand):
    help = 'Generate availability slots for all services'

    def handle(self, *args, **kwargs):
        services = Service.objects.filter(is_active=True)

        if not services.exists():
            self.stdout.write(self.style.WARNING('No active services found. Please create services first.'))
            return

        self.stdout.write(self.style.SUCCESS(f'Found {services.count()} active services'))

        # Delete existing availability to avoid duplicates
        deleted_count = Availability.objects.all().count()
        Availability.objects.all().delete()
        self.stdout.write(self.style.WARNING(f'Deleted {deleted_count} existing availability slots'))

        total_created = 0
        today = datetime.now().date()

        for service in services:
            provider = service.provider
            self.stdout.write(f'\nGenerating availability for: {service.name} (Provider: {provider.username})')

            # Generate availability for next 30 days
            for day_offset in range(30):
                current_date = today + timedelta(days=day_offset)

                # Skip some random days to make it more realistic
                if random.random() < 0.2:  # 20% chance to skip a day
                    continue

                # Determine working hours based on service category
                if service.category in ['salon_beauty', 'health_wellness']:
                    # 9 AM to 6 PM
                    start_hour = 9
                    end_hour = 18
                elif service.category in ['fitness', 'education']:
                    # 8 AM to 8 PM
                    start_hour = 8
                    end_hour = 20
                else:
                    # 10 AM to 5 PM
                    start_hour = 10
                    end_hour = 17

                # Generate time slots based on service duration
                duration_minutes = service.duration
                current_time = time(start_hour, 0)
                end_time_limit = time(end_hour, 0)

                slots_created = 0
                while True:
                    # Calculate end time for this slot
                    current_datetime = datetime.combine(current_date, current_time)
                    slot_end_datetime = current_datetime + timedelta(minutes=duration_minutes)
                    slot_end_time = slot_end_datetime.time()

                    # Check if this slot would go past end hour
                    if slot_end_time > end_time_limit:
                        break

                    # Randomly mark some slots as unavailable (already booked)
                    is_available = random.random() > 0.3  # 70% chance to be available

                    # Create availability slot
                    Availability.objects.create(
                        provider=provider,
                        service=service,
                        date=current_date,
                        start_time=current_time,
                        end_time=slot_end_time,
                        is_available=is_available
                    )

                    slots_created += 1
                    total_created += 1

                    # Move to next slot
                    next_datetime = current_datetime + timedelta(minutes=duration_minutes)
                    current_time = next_datetime.time()

                self.stdout.write(
                    self.style.SUCCESS(
                        f'  {current_date.strftime("%Y-%m-%d")}: Created {slots_created} slots'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Successfully generated {total_created} availability slots for {services.count()} services'
            )
        )

        # Show summary statistics
        available_slots = Availability.objects.filter(is_available=True).count()
        unavailable_slots = Availability.objects.filter(is_available=False).count()

        self.stdout.write(self.style.SUCCESS(f'\nSummary:'))
        self.stdout.write(self.style.SUCCESS(f'  Available slots: {available_slots}'))
        self.stdout.write(self.style.SUCCESS(f'  Booked slots: {unavailable_slots}'))
        self.stdout.write(self.style.SUCCESS(f'  Total slots: {total_created}'))
