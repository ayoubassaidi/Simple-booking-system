# bookings/models.py
from django.db import models
from django.contrib.auth.models import User


class Availability(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.provider.username} | {self.date} {self.start_time}-{self.end_time}"
