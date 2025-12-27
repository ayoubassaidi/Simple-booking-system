# bookings/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
from .models import Availability, Provider, Booking


@login_required
def add_availability(request):
    # Ensure only providers can access
    profile = UserProfile.objects.get(user=request.user)
    if profile.user_type != "provider":
        return redirect("dashboard")

    if request.method == "POST":
        Availability.objects.create(
            provider=request.user,
            date=request.POST.get("date"),
            start_time=request.POST.get("start_time"),
            end_time=request.POST.get("end_time"),
        )
        return redirect("add_availability")

    slots = Availability.objects.filter(provider=request.user).order_by("date")

    return render(request, "bookings/add_availability.html", {
        "slots": slots
    })


# Browse Service Providers - Simple View
def browse_providers(request):
    # Start with all providers
    providers = Provider.objects.all()

    # Get search parameters from URL
    service_type = request.GET.get('service_type', '')
    location = request.GET.get('location', '')
    sort_by = request.GET.get('sort_by', 'rating')

    # Filter by service type if selected
    if service_type:
        providers = providers.filter(service_type=service_type)

    # Filter by location if selected
    if location:
        providers = providers.filter(location=location)

    # Sort providers
    if sort_by == 'rating':
        providers = providers.order_by('-rating')
    elif sort_by == 'experience':
        providers = providers.order_by('-years_experience')
    elif sort_by == 'jobs':
        providers = providers.order_by('-completed_jobs')

    # Get all choices for dropdown filters
    service_choices = Provider.SERVICE_CHOICES
    location_choices = Provider.LOCATION_CHOICES

    # Pass everything to template
    context = {
        'providers': providers,
        'service_choices': service_choices,
        'location_choices': location_choices,
        'selected_service': service_type,
        'selected_location': location,
        'selected_sort': sort_by,
    }

    return render(request, 'bookings/browse_providers.html', context)


@login_required
def provider_bookings(request):
    profile = UserProfile.objects.get(user=request.user)
    if profile.user_type != "provider":
        return redirect("dashboard")

    bookings = Booking.objects.filter(
        provider=request.user
    ).select_related("customer").order_by("-date")

    return render(request, "bookings/provider_bookings.html", {
        "bookings": bookings
    })
