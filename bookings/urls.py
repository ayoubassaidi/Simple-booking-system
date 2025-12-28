from django.urls import path
from .views import (
    add_availability,
    browse_providers,
    my_services,
    add_service,
    edit_service,
    delete_service,
    toggle_service_status,
    search_services,
    view_availability,
    provider_bookings,
    confirm_booking,
    my_bookings,
    cancel_booking,
)

urlpatterns = [
    path("add-availability/", add_availability, name="add_availability"),
    path("browse-providers/", browse_providers, name="browse_providers"),
    path("search/", search_services, name="search_services"),
    path("service/<int:service_id>/availability/",
         view_availability, name="view_availability"),

    # Service Management URLs
    path("my-services/", my_services, name="my_services"),
    path("services/add/", add_service, name="add_service"),
    path("services/<int:service_id>/edit/", edit_service, name="edit_service"),
    path("services/<int:service_id>/delete/",
         delete_service, name="delete_service"),
    path("services/<int:service_id>/toggle/",
         toggle_service_status, name="toggle_service_status"),
    path("confirm/<int:service_id>/",
         confirm_booking,
         name="confirm_booking"
         ),


    path("provider/bookings/", provider_bookings, name="provider_bookings"),

    # Customer Bookings
    path('my-bookings/', my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/',
         cancel_booking, name='cancel_booking'),


]
