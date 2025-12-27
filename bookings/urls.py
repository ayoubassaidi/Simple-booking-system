from django.urls import path
from .views import add_availability, browse_providers, provider_bookings

urlpatterns = [
    path("add-availability/", add_availability, name="add_availability"),
    path("browse-providers/", browse_providers, name="browse_providers"),
    path("provider/bookings/", provider_bookings, name="provider_bookings"),

]
