"""
Management command to split existing long availability slots into multiple smaller slots
based on service duration. This fixes slots created before the auto-split feature was added.
"""

from django.core.management.base import BaseCommand
from bookings.models import Availability
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Splits existing long availability slots into multiple slots based on service duration'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Splitting Existing Availability Slots'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

        # Find all available slots
        long_slots = Availability.objects.filter(is_available=True)

        total_slots_processed = 0
        total_new_slots_created = 0
        slots_to_delete = []

        for slot in long_slots:
            # Calculate slot duration in minutes
            start_datetime = datetime.combine(slot.date, slot.start_time)
            end_datetime = datetime.combine(slot.date, slot.end_time)
            slot_duration = int((end_datetime - start_datetime).total_seconds() / 60)

            # Get service duration
            service_duration = slot.service.duration if slot.service else 60

            # Only split if the slot is longer than the service duration
            if slot_duration > service_duration:
                self.stdout.write(
                    f'\nProcessing: {slot.service.name if slot.service else "General"} '
                    f'on {slot.date} ({slot.start_time}-{slot.end_time}) '
                    f'[{slot_duration} min slot, {service_duration} min service]'
                )

                # Create multiple smaller slots
                current_slot_start = slot.start_time
                new_slots_count = 0

                while True:
                    # Calculate end time for this slot
                    current_start_datetime = datetime.combine(slot.date, current_slot_start)
                    slot_end_datetime = current_start_datetime + timedelta(minutes=service_duration)
                    current_slot_end = slot_end_datetime.time()

                    # Check if this slot goes beyond the original end time
                    if slot_end_datetime > end_datetime:
                        break

                    # Check if this exact slot already exists (avoid duplicates)
                    exists = Availability.objects.filter(
                        provider=slot.provider,
                        service=slot.service,
                        date=slot.date,
                        start_time=current_slot_start,
                        end_time=current_slot_end
                    ).exclude(id=slot.id).exists()

                    if not exists:
                        # Create new slot
                        Availability.objects.create(
                            provider=slot.provider,
                            service=slot.service,
                            date=slot.date,
                            start_time=current_slot_start,
                            end_time=current_slot_end,
                            is_available=True
                        )
                        new_slots_count += 1
                        self.stdout.write(
                            f'  ✓ Created: {current_slot_start} - {current_slot_end}'
                        )

                    # Move to next slot
                    current_slot_start = current_slot_end

                # Mark original slot for deletion
                if new_slots_count > 0:
                    slots_to_delete.append(slot)
                    total_new_slots_created += new_slots_count
                    total_slots_processed += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  → Split into {new_slots_count} smaller slots'
                        )
                    )

        # Delete original long slots
        if slots_to_delete:
            self.stdout.write(self.style.WARNING(f'\nDeleting {len(slots_to_delete)} original long slots...'))
            for slot in slots_to_delete:
                slot.delete()
            self.stdout.write(self.style.SUCCESS('✓ Original slots deleted'))

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS('MIGRATION COMPLETED'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS(f'✓ Long slots processed: {total_slots_processed}'))
        self.stdout.write(self.style.SUCCESS(f'✓ New smaller slots created: {total_new_slots_created}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Original long slots deleted: {len(slots_to_delete)}'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

        if total_slots_processed == 0:
            self.stdout.write(self.style.WARNING('\nNo long slots found that needed splitting!'))
            self.stdout.write(self.style.WARNING('All existing slots are already the correct duration.'))
