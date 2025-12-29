from django.apps import AppConfig


class BookingsConfig(AppConfig):
    name = 'bookings'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import bookings.signals  # Register signals
