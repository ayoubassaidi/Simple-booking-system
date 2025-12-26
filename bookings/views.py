# bookings/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
from .models import Availability


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
