from django.urls import path
from .views import add_availability

urlpatterns = [
    path("add-availability/", add_availability, name="add_availability"),
]
