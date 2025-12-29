# bookings/models.py
from django.db import models
from django.contrib.auth.models import User


# OLD DEPRECATED PROVIDER MODEL - NOT IN USE
# This old model is kept for historical data only (4 entries)
# DO NOT USE THIS MODEL - Use the ProviderProfile model below instead
class OldProvider(models.Model):
    # Service Type Choices
    SERVICE_CHOICES = [
        ('plumbing', 'Plumbing'),
        ('salon', 'Salon & Beauty'),
        ('therapy', 'Therapy'),
        ('cleaning', 'Cleaning'),
        ('tutoring', 'Tutoring'),
        ('other', 'Other'),
    ]

    # Location Choices
    LOCATION_CHOICES = [
        ('amsterdam', 'Amsterdam'),
        ('rotterdam', 'Rotterdam'),
        ('utrecht', 'Utrecht'),
        ('den_haag', 'Den Haag'),
    ]

    # Basic Information
    name = models.CharField(max_length=200)
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)

    # Rating and Stats
    rating = models.FloatField(default=0.0)
    years_experience = models.IntegerField(default=0)
    completed_jobs = models.IntegerField(default=0)

    # Details
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)

    # When was this provider added
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bookings_provider'  # Keep old table name
        verbose_name = 'Old Provider (Deprecated)'
        verbose_name_plural = 'Old Providers (Deprecated)'

    def __str__(self):
        return f"{self.name} - {self.get_service_type_display()}"

    # Helper method to get star rating display
    def get_stars(self):
        return '⭐' * int(self.rating)


# NEW PROVIDER MODEL - Dedicated table for service providers
class ProviderProfile(models.Model):
    """Dedicated provider profile table - separate from regular users"""

    SERVICE_TYPE_CHOICES = [
        ('salon_beauty', 'Salon & Beauty'),
        ('health_wellness', 'Health & Wellness'),
        ('education', 'Education & Tutoring'),
        ('home_services', 'Home Services'),
        ('fitness', 'Fitness & Sports'),
        ('technology', 'Technology & IT'),
        ('business', 'Business & Consulting'),
        ('other', 'Other'),
    ]

    # Link to User account
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='provider_profile',
        help_text="User account for this provider"
    )

    # Business Information
    business_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Business or trading name"
    )
    kvk_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="KVK (Chamber of Commerce) number"
    )

    # Service Information
    service_type = models.CharField(
        max_length=50,
        choices=SERVICE_TYPE_CHOICES,
        help_text="Primary service category"
    )
    bio = models.TextField(
        help_text="About the provider and their services"
    )

    # Location
    city = models.CharField(
        max_length=100,
        help_text="City where services are provided"
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Full address (optional)"
    )

    # Contact
    phone_number = models.CharField(
        max_length=20,
        help_text="Contact phone number"
    )
    website = models.URLField(
        blank=True,
        null=True,
        help_text="Website URL (optional)"
    )

    # Experience & Stats
    years_experience = models.IntegerField(
        default=0,
        help_text="Years of professional experience"
    )
    rating = models.FloatField(
        default=0.0,
        help_text="Average rating (0-5)"
    )
    total_bookings = models.IntegerField(
        default=0,
        help_text="Total number of completed bookings"
    )

    # Status
    is_verified = models.BooleanField(
        default=False,
        help_text="Has the provider been verified?"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Is the provider currently accepting bookings?"
    )

    # Profile Media
    profile_image = models.URLField(
        blank=True,
        null=True,
        help_text="Profile image URL"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Provider Profile'
        verbose_name_plural = 'Provider Profiles'
        ordering = ['-created_at']

    def __str__(self):
        name = self.business_name or self.user.get_full_name() or self.user.username
        return f"{name} - {self.get_service_type_display()}"

    @property
    def display_name(self):
        """Get the best display name for the provider"""
        return self.business_name or self.user.get_full_name() or self.user.username

    def get_rating_stars(self):
        """Return star representation of rating"""
        return '⭐' * int(self.rating)

    @staticmethod
    def is_provider(user):
        """Check if a user is a provider (has a ProviderProfile)"""
        try:
            return hasattr(user, 'provider_profile') and user.provider_profile is not None
        except:
            return False

    @staticmethod
    def get_provider_profile(user):
        """Get the provider profile for a user, or None if not a provider"""
        try:
            return user.provider_profile
        except ProviderProfile.DoesNotExist:
            return None


class Availability(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='availability_slots',
                                null=True, blank=True, help_text="Which service is available during this time")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Availabilities'
        ordering = ['date', 'start_time']

    def __str__(self):
        service_info = f" - {self.service.name}" if self.service else ""
        return f"{self.provider.username} | {self.date} {self.start_time}-{self.end_time}{service_info}"


class Service(models.Model):
    """Services offered by service providers"""

    # Service Categories
    CATEGORY_CHOICES = [
        ('salon_beauty', 'Salon & Beauty'),
        ('health_wellness', 'Health & Wellness'),
        ('education', 'Education & Tutoring'),
        ('home_services', 'Home Services'),
        ('fitness', 'Fitness & Sports'),
        ('technology', 'Technology & IT'),
        ('business', 'Business & Consulting'),
        ('other', 'Other'),
    ]

    # Duration Choices
    DURATION_CHOICES = [
        (30, '30 minutes'),
        (60, '1 hour'),
        (90, '1.5 hours'),
        (120, '2 hours'),
        (180, '3 hours'),
        (240, '4 hours'),
    ]

    # Relationships
    provider = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='services')

    # Service Information
    name = models.CharField(
        max_length=200, help_text="e.g., Hair Styling, Math Tutoring")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(
        help_text="Describe what this service includes")

    # Pricing & Duration
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Price in EUR")
    duration = models.IntegerField(
        choices=DURATION_CHOICES, default=60, help_text="Service duration")

    # Status
    is_active = models.BooleanField(
        default=True, help_text="Is this service currently offered?")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return f"{self.name} - €{self.price}"

    def get_duration_display_short(self):
        """Returns duration in a short format"""
        hours = self.duration // 60
        minutes = self.duration % 60
        if hours and minutes:
            return f"{hours}h {minutes}m"
        elif hours:
            return f"{hours}h"
        else:
            return f"{minutes}m"


class Notification(models.Model):
    """Notification system for users and providers"""

    NOTIFICATION_TYPES = [
        ('booking', 'Booking'),
        ('cancellation', 'Cancellation'),
        ('reminder', 'Reminder'),
        ('system', 'System'),
        ('message', 'Message'),
    ]

    # Recipient
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications')

    # Notification details
    notification_type = models.CharField(
        max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()

    # Status
    is_read = models.BooleanField(default=False)

    # Optional link
    link = models.CharField(max_length=255, blank=True,
                            null=True, help_text="URL to redirect when clicked")

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Booking(models.Model):
    """Booking/Appointment model for tracking service bookings"""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    # Relationships
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings_as_customer'
    )
    provider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings_as_provider'
    )
    service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    # ADD THIS (IMPORTANT)
    availability = models.OneToOneField(
        Availability,
        on_delete=models.CASCADE,
        related_name='booking',
        help_text="Booked availability slot"
    )

    # Booking Details
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    # Pricing
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price at the time of booking"
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # Notes
    customer_notes = models.TextField(blank=True, null=True)
    provider_notes = models.TextField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SearchQuery(models.Model):
    """Track search queries for analytics and improvement"""

    query = models.CharField(
        max_length=255, help_text="Search query entered by user")
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             null=True, blank=True, related_name='search_queries')

    # Filters applied
    category = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    min_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    # Results
    results_count = models.IntegerField(default=0)
    clicked_service = models.ForeignKey(
        'Service', on_delete=models.SET_NULL, null=True, blank=True, related_name='search_clicks')

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Search Query'
        verbose_name_plural = 'Search Queries'
        indexes = [
            models.Index(fields=['query', '-created_at']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.query} ({self.results_count} results)"
