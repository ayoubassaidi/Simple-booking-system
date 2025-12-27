from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('provider', 'Service Provider'),
        ('superadmin', 'Super Administrator'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    # Common fields for both User and Provider
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # User-specific fields
    birthday = models.DateField(blank=True, null=True, help_text="Your date of birth")
    address = models.CharField(max_length=255, blank=True, null=True, help_text="Your full address")

    # Provider-specific fields
    city = models.CharField(max_length=100, blank=True, null=True, help_text="City where you provide services")
    bio = models.TextField(blank=True, null=True, help_text="Tell us about your services")
    service_type = models.CharField(max_length=200, blank=True, null=True, help_text="What kind of service do you provide?")
    kvk_number = models.CharField(max_length=20, blank=True, null=True, help_text="KVK (Chamber of Commerce) number")

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"
