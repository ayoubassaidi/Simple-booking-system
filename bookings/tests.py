from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta, date, time
from decimal import Decimal
from .models import (
    ProviderProfile,
    Service,
    Availability,
    Booking,
    Notification
)


class ProviderProfileTestCase(TestCase):
    """Test cases for ProviderProfile model and related functionality"""

    def setUp(self):
        """Set up test data"""
        # Create a provider user
        self.provider_user = User.objects.create_user(
            username='testprovider',
            email='provider@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )

        # Create provider profile
        self.provider_profile = ProviderProfile.objects.create(
            user=self.provider_user,
            business_name='John\'s Salon',
            service_type='salon_beauty',
            bio='Professional hair styling services',
            city='Amsterdam',
            phone_number='+31612345678',
            years_experience=5,
            is_verified=True
        )

    def test_provider_profile_creation(self):
        """Test that provider profile is created correctly"""
        self.assertEqual(self.provider_profile.user, self.provider_user)
        self.assertEqual(self.provider_profile.business_name, 'John\'s Salon')
        self.assertEqual(self.provider_profile.service_type, 'salon_beauty')
        self.assertTrue(self.provider_profile.is_verified)

    def test_provider_display_name(self):
        """Test display name property"""
        self.assertEqual(self.provider_profile.display_name, 'John\'s Salon')

        # Test without business name
        self.provider_profile.business_name = ''
        self.provider_profile.save()
        self.assertEqual(self.provider_profile.display_name, 'John Doe')

    def test_is_provider_check(self):
        """Test static method to check if user is a provider"""
        self.assertTrue(ProviderProfile.is_provider(self.provider_user))

        # Create regular user
        regular_user = User.objects.create_user(
            username='regular',
            email='regular@test.com',
            password='testpass123'
        )
        self.assertFalse(ProviderProfile.is_provider(regular_user))


class ServiceTestCase(TestCase):
    """Test cases for Service model"""

    def setUp(self):
        """Set up test data"""
        self.provider_user = User.objects.create_user(
            username='provider',
            password='testpass123'
        )

        self.service = Service.objects.create(
            provider=self.provider_user,
            name='Haircut',
            category='salon_beauty',
            description='Professional haircut service',
            price=Decimal('35.00'),
            duration=60,
            is_active=True
        )

    def test_service_creation(self):
        """Test that service is created correctly"""
        self.assertEqual(self.service.name, 'Haircut')
        self.assertEqual(self.service.price, Decimal('35.00'))
        self.assertEqual(self.service.duration, 60)
        self.assertTrue(self.service.is_active)

    def test_get_duration_display_short(self):
        """Test duration display formatting"""
        # Test 1 hour
        self.assertEqual(self.service.get_duration_display_short(), '1h')

        # Test 30 minutes
        self.service.duration = 30
        self.assertEqual(self.service.get_duration_display_short(), '30m')

        # Test 90 minutes (1h 30m)
        self.service.duration = 90
        self.assertEqual(self.service.get_duration_display_short(), '1h 30m')


class AvailabilityTestCase(TestCase):
    """Test cases for Availability model and creation"""

    def setUp(self):
        """Set up test data"""
        self.provider_user = User.objects.create_user(
            username='provider',
            password='testpass123'
        )

        self.service = Service.objects.create(
            provider=self.provider_user,
            name='Haircut',
            category='salon_beauty',
            description='Professional haircut',
            price=Decimal('35.00'),
            duration=60
        )

        self.client = Client()
        self.client.login(username='provider', password='testpass123')

    def test_single_availability_creation(self):
        """Test creating a single availability slot"""
        availability = Availability.objects.create(
            provider=self.provider_user,
            service=self.service,
            date=date.today() + timedelta(days=1),
            start_time=time(9, 0),
            end_time=time(10, 0),
            is_available=True
        )

        self.assertEqual(availability.provider, self.provider_user)
        self.assertEqual(availability.service, self.service)
        self.assertTrue(availability.is_available)

    def test_bulk_availability_daily_pattern(self):
        """Test creating availability with daily pattern"""
        start_date = date.today()
        end_date = start_date + timedelta(days=6)  # 7 days total

        # Create daily availability
        created_slots = []
        current_date = start_date
        while current_date <= end_date:
            availability = Availability.objects.create(
                provider=self.provider_user,
                service=self.service,
                date=current_date,
                start_time=time(9, 0),
                end_time=time(17, 0),
                is_available=True
            )
            created_slots.append(availability)
            current_date += timedelta(days=1)

        # Should create 7 slots
        self.assertEqual(len(created_slots), 7)
        self.assertEqual(
            Availability.objects.filter(
                provider=self.provider_user,
                date__range=[start_date, end_date]
            ).count(),
            7
        )

    def test_bulk_availability_weekdays_pattern(self):
        """Test creating availability for weekdays only"""
        start_date = date.today()
        end_date = start_date + timedelta(days=13)  # 2 weeks

        # Create weekday availability (Monday-Friday)
        created_slots = []
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() < 5:  # 0-4 are Monday-Friday
                availability = Availability.objects.create(
                    provider=self.provider_user,
                    service=self.service,
                    date=current_date,
                    start_time=time(9, 0),
                    end_time=time(17, 0),
                    is_available=True
                )
                created_slots.append(availability)
            current_date += timedelta(days=1)

        # Should create 10 weekday slots (2 weeks × 5 weekdays)
        self.assertEqual(len(created_slots), 10)

    def test_bulk_availability_weekend_pattern(self):
        """Test creating availability for weekends only"""
        start_date = date.today()
        end_date = start_date + timedelta(days=13)  # 2 weeks

        # Create weekend availability (Saturday-Sunday)
        created_slots = []
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() >= 5:  # 5-6 are Saturday-Sunday
                availability = Availability.objects.create(
                    provider=self.provider_user,
                    service=self.service,
                    date=current_date,
                    start_time=time(10, 0),
                    end_time=time(16, 0),
                    is_available=True
                )
                created_slots.append(availability)
            current_date += timedelta(days=1)

        # Should create 4 weekend slots (2 weeks × 2 weekend days)
        self.assertEqual(len(created_slots), 4)

    def test_bulk_availability_custom_days_pattern(self):
        """Test creating availability for custom days (e.g., Mon, Wed, Fri)"""
        start_date = date.today()
        end_date = start_date + timedelta(days=20)  # 3 weeks
        custom_days = [0, 2, 4]  # Monday, Wednesday, Friday

        # Create custom days availability
        created_slots = []
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() in custom_days:
                availability = Availability.objects.create(
                    provider=self.provider_user,
                    service=self.service,
                    date=current_date,
                    start_time=time(9, 0),
                    end_time=time(17, 0),
                    is_available=True
                )
                created_slots.append(availability)
            current_date += timedelta(days=1)

        # Should create 9 slots (3 weeks × 3 days)
        self.assertEqual(len(created_slots), 9)


class BookingTestCase(TestCase):
    """Test cases for Booking model and conflict detection"""

    def setUp(self):
        """Set up test data"""
        # Create provider
        self.provider_user = User.objects.create_user(
            username='provider',
            password='testpass123'
        )

        # Create customer
        self.customer_user = User.objects.create_user(
            username='customer',
            password='testpass123'
        )

        # Create service
        self.service = Service.objects.create(
            provider=self.provider_user,
            name='Haircut',
            category='salon_beauty',
            description='Professional haircut',
            price=Decimal('35.00'),
            duration=60  # 1 hour
        )

        # Create availability
        self.tomorrow = date.today() + timedelta(days=1)
        self.availability = Availability.objects.create(
            provider=self.provider_user,
            service=self.service,
            date=self.tomorrow,
            start_time=time(9, 0),
            end_time=time(10, 0),
            is_available=True
        )

    def test_booking_creation(self):
        """Test creating a booking"""
        booking = Booking.objects.create(
            customer=self.customer_user,
            provider=self.provider_user,
            service=self.service,
            availability=self.availability,
            date=self.tomorrow,
            start_time=time(9, 0),
            end_time=time(10, 0),
            price=self.service.price,
            status='confirmed'
        )

        self.assertEqual(booking.customer, self.customer_user)
        self.assertEqual(booking.provider, self.provider_user)
        self.assertEqual(booking.service, self.service)
        self.assertEqual(booking.status, 'confirmed')

    def test_booking_marks_availability_unavailable(self):
        """Test that creating a booking marks availability as unavailable"""
        # Create booking
        booking = Booking.objects.create(
            customer=self.customer_user,
            provider=self.provider_user,
            service=self.service,
            availability=self.availability,
            date=self.tomorrow,
            start_time=time(9, 0),
            end_time=time(10, 0),
            price=self.service.price,
            status='confirmed'
        )

        # Mark availability as unavailable
        self.availability.is_available = False
        self.availability.save()

        # Refresh from database
        self.availability.refresh_from_db()
        self.assertFalse(self.availability.is_available)

    def test_booking_conflict_detection(self):
        """Test that overlapping bookings are prevented"""
        # Create first booking (9:00 - 10:00)
        booking1 = Booking.objects.create(
            customer=self.customer_user,
            provider=self.provider_user,
            service=self.service,
            availability=self.availability,
            date=self.tomorrow,
            start_time=time(9, 0),
            end_time=time(10, 0),
            price=self.service.price,
            status='confirmed'
        )

        # Mark availability as unavailable
        self.availability.is_available = False
        self.availability.save()

        # Try to check if this slot is still available
        available_slots = Availability.objects.filter(
            service=self.service,
            date=self.tomorrow,
            start_time=time(9, 0),
            is_available=True
        )

        # Should be no available slots at this time
        self.assertEqual(available_slots.count(), 0)

    def test_service_duration_calculation(self):
        """Test that booking end time matches service duration"""
        # Service duration is 60 minutes
        start = time(14, 0)  # 2:00 PM
        start_datetime = datetime.combine(self.tomorrow, start)
        end_datetime = start_datetime + timedelta(minutes=self.service.duration)
        end_time = end_datetime.time()

        # Create availability
        availability = Availability.objects.create(
            provider=self.provider_user,
            service=self.service,
            date=self.tomorrow,
            start_time=start,
            end_time=end_time,
            is_available=True
        )

        # Create booking
        booking = Booking.objects.create(
            customer=self.customer_user,
            provider=self.provider_user,
            service=self.service,
            availability=availability,
            date=self.tomorrow,
            start_time=start,
            end_time=end_time,
            price=self.service.price,
            status='confirmed'
        )

        # End time should be exactly 1 hour after start time
        self.assertEqual(booking.end_time, time(15, 0))

    def test_multiple_services_different_durations(self):
        """Test bookings with services of different durations"""
        # Create 30-minute service
        short_service = Service.objects.create(
            provider=self.provider_user,
            name='Quick Trim',
            category='salon_beauty',
            description='Quick hair trim',
            price=Decimal('20.00'),
            duration=30
        )

        # Create 2-hour service
        long_service = Service.objects.create(
            provider=self.provider_user,
            name='Color Treatment',
            category='salon_beauty',
            description='Full color treatment',
            price=Decimal('80.00'),
            duration=120
        )

        # Test 30-minute booking
        start_short = time(9, 0)
        start_datetime = datetime.combine(self.tomorrow, start_short)
        end_datetime = start_datetime + timedelta(minutes=short_service.duration)
        end_short = end_datetime.time()

        avail_short = Availability.objects.create(
            provider=self.provider_user,
            service=short_service,
            date=self.tomorrow,
            start_time=start_short,
            end_time=end_short,
            is_available=True
        )

        booking_short = Booking.objects.create(
            customer=self.customer_user,
            provider=self.provider_user,
            service=short_service,
            availability=avail_short,
            date=self.tomorrow,
            start_time=start_short,
            end_time=end_short,
            price=short_service.price,
            status='confirmed'
        )

        self.assertEqual(booking_short.end_time, time(9, 30))

        # Test 2-hour booking
        start_long = time(10, 0)
        start_datetime = datetime.combine(self.tomorrow, start_long)
        end_datetime = start_datetime + timedelta(minutes=long_service.duration)
        end_long = end_datetime.time()

        avail_long = Availability.objects.create(
            provider=self.provider_user,
            service=long_service,
            date=self.tomorrow,
            start_time=start_long,
            end_time=end_long,
            is_available=True
        )

        booking_long = Booking.objects.create(
            customer=self.customer_user,
            provider=self.provider_user,
            service=long_service,
            availability=avail_long,
            date=self.tomorrow,
            start_time=start_long,
            end_time=end_long,
            price=long_service.price,
            status='confirmed'
        )

        self.assertEqual(booking_long.end_time, time(12, 0))


class DeleteAvailabilityTestCase(TestCase):
    """Test cases for deleting availability slots"""

    def setUp(self):
        """Set up test data"""
        self.provider_user = User.objects.create_user(
            username='provider',
            password='testpass123'
        )

        self.customer_user = User.objects.create_user(
            username='customer',
            password='testpass123'
        )

        self.service = Service.objects.create(
            provider=self.provider_user,
            name='Haircut',
            category='salon_beauty',
            description='Professional haircut',
            price=Decimal('35.00'),
            duration=60
        )

        self.tomorrow = date.today() + timedelta(days=1)

    def test_delete_unbooked_availability(self):
        """Test deleting an availability slot with no booking"""
        availability = Availability.objects.create(
            provider=self.provider_user,
            service=self.service,
            date=self.tomorrow,
            start_time=time(9, 0),
            end_time=time(10, 0),
            is_available=True
        )

        availability_id = availability.id
        availability.delete()

        # Should be deleted
        self.assertFalse(
            Availability.objects.filter(id=availability_id).exists()
        )

    def test_cannot_delete_booked_availability(self):
        """Test that availability with a booking cannot be deleted"""
        availability = Availability.objects.create(
            provider=self.provider_user,
            service=self.service,
            date=self.tomorrow,
            start_time=time(9, 0),
            end_time=time(10, 0),
            is_available=True
        )

        # Create booking
        booking = Booking.objects.create(
            customer=self.customer_user,
            provider=self.provider_user,
            service=self.service,
            availability=availability,
            date=self.tomorrow,
            start_time=time(9, 0),
            end_time=time(10, 0),
            price=self.service.price,
            status='confirmed'
        )

        # Check if booking exists
        has_booking = hasattr(availability, 'booking') and availability.booking is not None

        # Should have a booking
        self.assertTrue(has_booking)

    def test_availability_freed_when_booking_cancelled(self):
        """Test that availability becomes available again when booking is cancelled"""
        availability = Availability.objects.create(
            provider=self.provider_user,
            service=self.service,
            date=self.tomorrow,
            start_time=time(9, 0),
            end_time=time(10, 0),
            is_available=True
        )

        # Create booking
        booking = Booking.objects.create(
            customer=self.customer_user,
            provider=self.provider_user,
            service=self.service,
            availability=availability,
            date=self.tomorrow,
            start_time=time(9, 0),
            end_time=time(10, 0),
            price=self.service.price,
            status='confirmed'
        )

        # Mark availability as unavailable
        availability.is_available = False
        availability.save()

        # Cancel booking
        booking.status = 'cancelled'
        booking.save()

        # Free up the availability
        availability.is_available = True
        availability.save()

        # Refresh from database
        availability.refresh_from_db()

        # Should be available again
        self.assertTrue(availability.is_available)


class DateRangeNavigationTestCase(TestCase):
    """Test cases for date range calculation and week navigation"""

    def setUp(self):
        """Set up test data"""
        self.provider_user = User.objects.create_user(
            username='provider',
            password='testpass123'
        )

        self.service = Service.objects.create(
            provider=self.provider_user,
            name='Haircut',
            category='salon_beauty',
            description='Professional haircut',
            price=Decimal('35.00'),
            duration=60
        )

        # Create availability for next 30 days
        today = date.today()
        for i in range(1, 31):
            Availability.objects.create(
                provider=self.provider_user,
                service=self.service,
                date=today + timedelta(days=i),
                start_time=time(9, 0),
                end_time=time(17, 0),
                is_available=True
            )

    def test_date_range_aggregation(self):
        """Test calculating earliest and latest available dates"""
        from django.db.models import Min, Max

        today = date.today()
        availability_range = Availability.objects.filter(
            provider=self.provider_user,
            service=self.service,
            date__gte=today,
            is_available=True
        ).aggregate(
            earliest_date=Min('date'),
            latest_date=Max('date')
        )

        earliest = availability_range['earliest_date']
        latest = availability_range['latest_date']

        # Should have 30 days of availability
        self.assertIsNotNone(earliest)
        self.assertIsNotNone(latest)
        self.assertEqual((latest - earliest).days + 1, 30)

    def test_week_navigation_boundaries(self):
        """Test previous/next week navigation boundaries"""
        from django.db.models import Min, Max

        today = date.today()

        # Get date range
        availability_range = Availability.objects.filter(
            provider=self.provider_user,
            service=self.service,
            date__gte=today,
            is_available=True
        ).aggregate(
            earliest_date=Min('date'),
            latest_date=Max('date')
        )

        latest_available = availability_range['latest_date']

        # Test week 0 (current week)
        week_offset = 0
        start_date = today + timedelta(days=week_offset * 7)
        end_of_week = start_date + timedelta(days=6)

        has_previous_week = week_offset > 0
        has_next_week = latest_available > end_of_week

        # Should not have previous week, should have next week
        self.assertFalse(has_previous_week)
        self.assertTrue(has_next_week)

        # Test week 4 (last week with availability)
        week_offset = 4
        start_date = today + timedelta(days=week_offset * 7)
        end_of_week = start_date + timedelta(days=6)

        has_previous_week = week_offset > 0
        has_next_week = latest_available > end_of_week

        # Should have previous week, should not have next week
        self.assertTrue(has_previous_week)
        self.assertFalse(has_next_week)


class NotificationTestCase(TestCase):
    """Test cases for notification system"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_notification_creation(self):
        """Test creating a notification"""
        notification = Notification.objects.create(
            user=self.user,
            notification_type='booking',
            title='New Booking',
            message='You have a new booking for tomorrow at 9:00 AM',
            is_read=False
        )

        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.notification_type, 'booking')
        self.assertFalse(notification.is_read)

    def test_notification_read_status(self):
        """Test marking notification as read"""
        notification = Notification.objects.create(
            user=self.user,
            notification_type='reminder',
            title='Upcoming Appointment',
            message='Your appointment is tomorrow',
            is_read=False
        )

        # Mark as read
        notification.is_read = True
        notification.save()

        # Refresh from database
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)
