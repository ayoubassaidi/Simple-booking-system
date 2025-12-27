# bookings/models.py
from django.db import models
from django.contrib.auth.models import User


# Service Provider Model - Simple and Easy to Understand
class Provider(models.Model):
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

    def __str__(self):
        return f"{self.name} - {self.get_service_type_display()}"

    # Helper method to get star rating display
    def get_stars(self):
        return '⭐' * int(self.rating)


class Availability(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.provider.username} | {self.date} {self.start_time}-{self.end_time}"


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    customer = models.ForeignKey(
        User, related_name="customer_bookings", on_delete=models.CASCADE
    )
    provider = models.ForeignKey(
        User, related_name="provider_bookings", on_delete=models.CASCADE
    )

    service_type = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} → {self.provider.username}"
