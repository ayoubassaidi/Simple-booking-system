# bookings/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Min, Max
from accounts.models import UserProfile
from .models import Availability, Service, SearchQuery, Booking, ProviderProfile
from .forms import ServiceForm


@login_required
def add_availability(request):
    """Add availability slots - supports both single and bulk creation"""
    from datetime import datetime, timedelta

    # Ensure only providers can access
    if not ProviderProfile.is_provider(request.user):
        messages.error(request, "Only service providers can access this page.")
        return redirect("dashboard")

    # Get provider's services for the dropdown
    provider_services = Service.objects.filter(
        provider=request.user, is_active=True)

    if request.method == "POST":
        service_id = request.POST.get("service")
        service = None

        if service_id:
            service = Service.objects.get(id=service_id, provider=request.user)

        # Check if this is bulk creation or single slot
        mode = request.POST.get("mode", "single")

        if mode == "bulk":
            # Bulk creation logic
            start_date_str = request.POST.get("start_date")
            end_date_str = request.POST.get("end_date")
            start_time_str = request.POST.get("start_time")
            end_time_str = request.POST.get("end_time")
            repeat_pattern = request.POST.get("repeat_pattern", "daily")
            selected_days = request.POST.getlist("selected_days")  # For weekly pattern

            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                start_time = datetime.strptime(start_time_str, '%H:%M').time()
                end_time = datetime.strptime(end_time_str, '%H:%M').time()

                slots_created = 0
                current_date = start_date

                # Get service duration (in minutes)
                service_duration = service.duration if service else 60  # Default to 60 minutes

                while current_date <= end_date:
                    should_create = False

                    if repeat_pattern == "daily":
                        should_create = True
                    elif repeat_pattern == "weekdays":
                        # Monday = 0, Sunday = 6
                        should_create = current_date.weekday() < 5
                    elif repeat_pattern == "weekends":
                        should_create = current_date.weekday() >= 5
                    elif repeat_pattern == "custom" and selected_days:
                        # selected_days contains day names like ['monday', 'wednesday', 'friday']
                        day_name = current_date.strftime('%A').lower()
                        should_create = day_name in selected_days

                    if should_create:
                        # Split the time range into slots based on service duration
                        current_slot_start = start_time

                        while True:
                            # Calculate end time for this slot
                            start_datetime = datetime.combine(current_date, current_slot_start)
                            slot_end_datetime = start_datetime + timedelta(minutes=service_duration)
                            current_slot_end = slot_end_datetime.time()

                            # Check if this slot goes beyond the end time
                            end_datetime = datetime.combine(current_date, end_time)
                            if slot_end_datetime > end_datetime:
                                break

                            # Check if slot already exists to avoid duplicates
                            exists = Availability.objects.filter(
                                provider=request.user,
                                service=service,
                                date=current_date,
                                start_time=current_slot_start,
                                end_time=current_slot_end
                            ).exists()

                            if not exists:
                                Availability.objects.create(
                                    provider=request.user,
                                    service=service,
                                    date=current_date,
                                    start_time=current_slot_start,
                                    end_time=current_slot_end,
                                )
                                slots_created += 1

                            # Move to next slot
                            current_slot_start = current_slot_end

                    current_date += timedelta(days=1)

                messages.success(request, f"Successfully created {slots_created} availability slots!")
                return redirect("add_availability")

            except Exception as e:
                messages.error(request, f"Error creating bulk availability: {str(e)}")
                return redirect("add_availability")
        else:
            # Single slot creation (original logic)
            Availability.objects.create(
                provider=request.user,
                service=service,
                date=request.POST.get("date"),
                start_time=request.POST.get("start_time"),
                end_time=request.POST.get("end_time"),
            )
            messages.success(request, "Availability slot added successfully!")
            return redirect("add_availability")

    # Get slots ordered by most recent first, then show upcoming slots
    from datetime import date as date_today
    today = date_today.today()

    slots = Availability.objects.filter(
        provider=request.user,
        date__gte=today  # Only show today and future slots
    ).select_related('service').order_by("-date", "-start_time")  # Most recent first

    return render(request, "bookings/add_availability.html", {
        "slots": slots,
        "provider_services": provider_services,
    })


# Browse Service Providers - Shows all active services
def browse_providers(request):
    # Start with all active services
    services = Service.objects.filter(
        is_active=True).select_related('provider')

    # Get search parameters from URL
    category = request.GET.get('category', '')
    search = request.GET.get('search', '')
    sort_by = request.GET.get('sort_by', 'newest')

    # Filter by category if selected
    if category:
        services = services.filter(category=category)

    # Search by service name or description
    if search:
        services = services.filter(
            name__icontains=search
        ) | services.filter(
            description__icontains=search
        )

    # Sort services
    if sort_by == 'newest':
        services = services.order_by('-created_at')
    elif sort_by == 'price_low':
        services = services.order_by('price')
    elif sort_by == 'price_high':
        services = services.order_by('-price')
    elif sort_by == 'duration':
        services = services.order_by('duration')

    # Get category choices for dropdown
    category_choices = Service.CATEGORY_CHOICES

    # Pass everything to template
    context = {
        'services': services,
        'category_choices': category_choices,
        'selected_category': category,
        'search_query': search,
        'selected_sort': sort_by,
    }

    return render(request, 'bookings/browse_providers.html', context)


# ==========================================
# SERVICE MANAGEMENT VIEWS (Providers Only)
# ==========================================

@login_required
def my_services(request):
    """List all services for the logged-in provider"""
    # Ensure only providers can access
    if not ProviderProfile.is_provider(request.user):
        messages.error(request, 'Only service providers can manage services.')
        return redirect('dashboard')

    # Get all services for this provider
    services = Service.objects.filter(provider=request.user)

    # Calculate stats
    total_services = services.count()
    active_services = services.filter(is_active=True).count()
    inactive_services = services.filter(is_active=False).count()

    context = {
        'services': services,
        'total_services': total_services,
        'active_services': active_services,
        'inactive_services': inactive_services,
    }

    return render(request, 'bookings/my_services.html', context)


@login_required
def add_service(request):
    """Add a new service"""
    # Ensure only providers can access
    if not ProviderProfile.is_provider(request.user):
        messages.error(request, 'Only service providers can add services.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user
            service.save()
            messages.success(
                request, f'Service "{service.name}" added successfully!')
            return redirect('my_services')
    else:
        form = ServiceForm()

    context = {
        'form': form,
        'form_title': 'Add New Service',
        'button_text': 'Add Service',
    }

    return render(request, 'bookings/service_form.html', context)


@login_required
def edit_service(request, service_id):
    """Edit an existing service"""
    # Get the service and ensure it belongs to the logged-in provider
    service = get_object_or_404(Service, id=service_id, provider=request.user)

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Service "{service.name}" updated successfully!')
            return redirect('my_services')
    else:
        form = ServiceForm(instance=service)

    context = {
        'form': form,
        'service': service,
        'form_title': 'Edit Service',
        'button_text': 'Update Service',
    }

    return render(request, 'bookings/service_form.html', context)


@login_required
def delete_service(request, service_id):
    """Delete a service"""
    service = get_object_or_404(Service, id=service_id, provider=request.user)

    if request.method == 'POST':
        service_name = service.name
        service.delete()
        messages.success(
            request, f'Service "{service_name}" deleted successfully!')
        return redirect('my_services')

    context = {
        'service': service,
    }

    return render(request, 'bookings/service_confirm_delete.html', context)


@login_required
def toggle_service_status(request, service_id):
    """Toggle service active/inactive status"""
    service = get_object_or_404(Service, id=service_id, provider=request.user)

    service.is_active = not service.is_active
    service.save()

    status_text = 'activated' if service.is_active else 'deactivated'
    messages.success(
        request, f'Service "{service.name}" {status_text} successfully!')

    return redirect('my_services')


# ==========================================
# SMART SEARCH VIEW
# ==========================================

def search_services(request):
    """Smart search functionality with query tracking"""
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort_by = request.GET.get('sort_by', 'relevance')

    # Start with all active services
    services = Service.objects.filter(
        is_active=True).select_related('provider')

    # Apply search query - search across service name, description, and provider name
    if query:
        services = services.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(provider__username__icontains=query) |
            Q(provider__first_name__icontains=query) |
            Q(provider__last_name__icontains=query)
        )

    # Filter by category
    if category:
        services = services.filter(category=category)

    # Filter by price range
    if min_price:
        try:
            services = services.filter(price__gte=float(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            services = services.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Sort results
    if sort_by == 'price_low':
        services = services.order_by('price')
    elif sort_by == 'price_high':
        services = services.order_by('-price')
    elif sort_by == 'duration':
        services = services.order_by('duration')
    elif sort_by == 'newest':
        services = services.order_by('-created_at')
    else:  # relevance (default)
        services = services.order_by('-created_at')

    results_count = services.count()

    # Track the search query for analytics
    if query or category:
        try:
            search_query = SearchQuery.objects.create(
                query=query,
                user=request.user if request.user.is_authenticated else None,
                category=category if category else None,
                min_price=float(min_price) if min_price else None,
                max_price=float(max_price) if max_price else None,
                results_count=results_count,
                ip_address=request.META.get('REMOTE_ADDR')
            )
        except Exception:
            pass  # Don't fail if search tracking fails

    # Get category choices for filter dropdown
    category_choices = Service.CATEGORY_CHOICES

    context = {
        'services': services,
        'search_query': query,
        'selected_category': category,
        'min_price': min_price,
        'max_price': max_price,
        'selected_sort': sort_by,
        'results_count': results_count,
        'category_choices': category_choices,
    }

    return render(request, 'bookings/search_results.html', context)


# ==========================================
# VIEW AVAILABILITY
# ==========================================

@login_required
def view_availability(request, service_id):
    """View availability calendar for a specific service - Only customers can view"""
    from datetime import datetime, timedelta

    # Prevent providers from viewing availability to book
    if ProviderProfile.is_provider(request.user):
        messages.error(
            request, "Service providers cannot book services. This page is only for customers.")
        return redirect("browse_providers")

    service = get_object_or_404(Service, id=service_id, is_active=True)

    # Get the selected date from query params or default to today
    selected_date_str = request.GET.get('date')
    if selected_date_str:
        try:
            selected_date = datetime.strptime(
                selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = datetime.now().date()
    else:
        selected_date = datetime.now().date()

    # Get availability date range for this service
    today = datetime.now().date()
    availability_range = Availability.objects.filter(
        provider=service.provider,
        service=service,
        date__gte=today,
        is_available=True
    ).aggregate(
        earliest_date=Min('date'),
        latest_date=Max('date')
    )

    earliest_available = availability_range['earliest_date'] or today
    latest_available = availability_range['latest_date'] or today

    # Calculate total available days
    total_available_days = (latest_available - earliest_available).days + 1 if latest_available >= earliest_available else 0

    # Get the week offset from query params (for navigation)
    week_offset = int(request.GET.get('week', 0))

    # Generate 7 days starting from the calculated start date
    start_date = today + timedelta(days=week_offset * 7)
    week_dates = []
    for i in range(7):
        date = start_date + timedelta(days=i)
        week_dates.append({
            'date': date,
            'day_name': date.strftime('%a'),
            'day_num': date.strftime('%d'),
            'is_selected': date == selected_date,
            'month': date.strftime('%B'),
            'year': date.year
        })

    # Calculate navigation info
    has_previous_week = week_offset > 0
    # Check if there are dates beyond current week view
    end_of_current_week = start_date + timedelta(days=6)
    has_next_week = latest_available > end_of_current_week

    # Get availability slots for the selected date
    availability_slots = Availability.objects.filter(
        provider=service.provider,
        service=service,
        date=selected_date
    ).order_by('start_time')

    # Get all bookings for this provider on the selected date to check for conflicts
    existing_bookings = Booking.objects.filter(
        provider=service.provider,
        date=selected_date,
        status__in=['pending', 'confirmed']  # Only active bookings block slots
    ).select_related('service')

    # Helper function to check if a time slot conflicts with any existing booking
    def is_slot_conflicting(slot_start, slot_end):
        """Check if proposed time slot conflicts with any existing booking"""
        for booking in existing_bookings:
            booking_start = datetime.combine(selected_date, booking.start_time)
            booking_end = datetime.combine(selected_date, booking.end_time)
            proposed_start = datetime.combine(selected_date, slot_start)
            proposed_end = datetime.combine(selected_date, slot_end)

            # Check for overlap: bookings overlap if one starts before the other ends
            if proposed_start < booking_end and proposed_end > booking_start:
                return True
        return False

    # Build time slots from availability, respecting service duration
    time_slots = []
    for slot in availability_slots:
        # Calculate the end time based on service duration
        slot_start_datetime = datetime.combine(selected_date, slot.start_time)
        slot_end_datetime = slot_start_datetime + timedelta(minutes=service.duration)
        calculated_end_time = slot_end_datetime.time()

        # Check if this slot conflicts with existing bookings
        has_conflict = is_slot_conflicting(slot.start_time, calculated_end_time)

        # Determine if slot is truly available
        is_truly_available = slot.is_available and not has_conflict

        time_slots.append({
            'id': slot.id,
            'time': slot.start_time.strftime('%H:%M'),
            'display_time': slot.start_time.strftime('%I:%M %p'),
            'end_time': calculated_end_time.strftime('%H:%M'),
            'is_available': is_truly_available
        })

    context = {
        'service': service,
        'week_dates': week_dates,
        'time_slots': time_slots,
        'selected_date': selected_date,
        'earliest_available': earliest_available,
        'latest_available': latest_available,
        'total_available_days': total_available_days,
        'current_week_offset': week_offset,
        'has_previous_week': has_previous_week,
        'has_next_week': has_next_week,
    }

    return render(request, 'bookings/view_availability.html', context)
# ==========================================
# Confirm booking
# ==========================================


@login_required
def confirm_booking(request, service_id):
    """Confirm a booking - Only customers can book, providers cannot"""
    # Prevent providers from booking services
    if ProviderProfile.is_provider(request.user):
        messages.error(
            request, "Service providers cannot book services. Only customers can make bookings.")
        return redirect("browse_providers")

    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("browse_providers")

    availability_id = request.POST.get("availability_id")

    # Debug logging
    print("=" * 50)
    print("CONFIRM BOOKING DEBUG")
    print("=" * 50)
    print(f"Service ID: {service_id}")
    print(f"Availability ID from POST: {availability_id}")
    print(f"All POST data: {request.POST}")
    print("=" * 50)

    if not availability_id:
        messages.error(request, "Please select a time slot.")
        return redirect("view_availability", service_id=service_id)

    try:
        availability = Availability.objects.get(
            id=availability_id,
            is_available=True
        )
    except Availability.DoesNotExist:
        messages.error(request, "Selected time slot is not available.")
        return redirect("view_availability", service_id=service_id)

    service = get_object_or_404(Service, id=service_id)

    # Prevent double booking
    if hasattr(availability, "booking"):
        messages.error(request, "This slot is already booked.")
        return redirect("view_availability", service_id=service_id)

    # CREATE BOOKING
    try:
        # Calculate end time based on service duration
        from datetime import datetime, timedelta
        start_datetime = datetime.combine(availability.date, availability.start_time)
        end_datetime = start_datetime + timedelta(minutes=service.duration)
        calculated_end_time = end_datetime.time()

        # Check for booking conflicts before creating
        conflicting_bookings = Booking.objects.filter(
            provider=availability.provider,
            date=availability.date,
            status__in=['pending', 'confirmed']
        )

        # Check if the new booking would overlap with any existing booking
        for existing_booking in conflicting_bookings:
            existing_start = datetime.combine(availability.date, existing_booking.start_time)
            existing_end = datetime.combine(availability.date, existing_booking.end_time)

            # Check for overlap
            if start_datetime < existing_end and end_datetime > existing_start:
                messages.error(request, "This time slot conflicts with an existing booking. Please choose another time.")
                return redirect("view_availability", service_id=service_id)

        booking = Booking.objects.create(
            customer=request.user,
            provider=availability.provider,
            service=service,
            availability=availability,
            date=availability.date,
            start_time=availability.start_time,
            end_time=calculated_end_time,  # Use calculated end time based on duration
            price=service.price,
            status="pending"
        )

        # Mark slot unavailable
        availability.is_available = False
        availability.save()

        # Mark any other availability slots that would conflict as unavailable
        overlapping_slots = Availability.objects.filter(
            provider=availability.provider,
            service=service,
            date=availability.date,
            is_available=True
        ).exclude(id=availability.id)

        for slot in overlapping_slots:
            slot_start = datetime.combine(availability.date, slot.start_time)
            slot_end_calc = slot_start + timedelta(minutes=service.duration)

            # If this slot would overlap with our new booking, mark it unavailable
            if slot_start < end_datetime and slot_end_calc > start_datetime:
                slot.is_available = False
                slot.save()

        messages.success(
            request, f"Booking request sent! Waiting for provider confirmation for {availability.date} at {availability.start_time}.")
        return redirect("my_bookings")

    except Exception as e:
        print(f"Error creating booking: {e}")
        messages.error(
            request, "An error occurred while creating your booking. Please try again.")
        return redirect("view_availability", service_id=service_id)


# ==========================================
# Bookings Page for Provider
# ==========================================

@login_required
def provider_bookings(request):
    if not ProviderProfile.is_provider(request.user):
        messages.error(request, "Only service providers can access this page.")
        return redirect("dashboard")

    # Handle booking actions (accept, reject, complete)
    if request.method == "POST":
        action = request.POST.get("action")
        booking_id = request.POST.get("booking_id")

        try:
            booking = Booking.objects.get(id=booking_id, provider=request.user)

            if action == "accept":
                booking.status = "confirmed"
                booking.save()
                messages.success(
                    request, f"Booking accepted for {booking.customer.username}")

            elif action == "reject":
                from datetime import datetime, timedelta

                booking.status = "cancelled"
                booking.save()

                # Make availability slot available again
                booking.availability.is_available = True
                booking.availability.save()

                # Free up overlapping slots that were blocked by this booking
                booking_start = datetime.combine(booking.date, booking.start_time)
                booking_end = datetime.combine(booking.date, booking.end_time)

                # Find all unavailable slots for this service on the same date
                overlapping_slots = Availability.objects.filter(
                    provider=booking.provider,
                    service=booking.service,
                    date=booking.date,
                    is_available=False
                ).exclude(id=booking.availability.id)

                # Check each slot to see if it was blocked by this booking
                for slot in overlapping_slots:
                    slot_start = datetime.combine(booking.date, slot.start_time)
                    slot_end_calc = slot_start + timedelta(minutes=booking.service.duration)

                    # If this slot was overlapping with the cancelled booking
                    if slot_start < booking_end and slot_end_calc > booking_start:
                        # Check if there are other active bookings blocking this slot
                        other_bookings = Booking.objects.filter(
                            provider=booking.provider,
                            date=booking.date,
                            status__in=['pending', 'confirmed']
                        ).exclude(id=booking.id)

                        slot_is_blocked = False
                        for other_booking in other_bookings:
                            other_start = datetime.combine(booking.date, other_booking.start_time)
                            other_end = datetime.combine(booking.date, other_booking.end_time)

                            if slot_start < other_end and slot_end_calc > other_start:
                                slot_is_blocked = True
                                break

                        # Only free the slot if no other bookings block it
                        if not slot_is_blocked:
                            slot.is_available = True
                            slot.save()

                messages.success(
                    request, f"Booking rejected for {booking.customer.username}")

            elif action == "complete":
                booking.status = "completed"
                booking.save()
                messages.success(request, f"Booking marked as completed")

        except Booking.DoesNotExist:
            messages.error(request, "Booking not found")

        return redirect("provider_bookings")

    # Get bookings categorized by status
    bookings = Booking.objects.filter(
        provider=request.user
    ).select_related("service", "customer").order_by("-date", "-start_time")

    pending_bookings = bookings.filter(status='pending')
    confirmed_bookings = bookings.filter(status='confirmed')
    completed_bookings = bookings.filter(status='completed')

    return render(request, "bookings/my_bookings_provider.html", {
        "bookings": bookings,
        "pending_bookings": pending_bookings,
        "confirmed_bookings": confirmed_bookings,
        "completed_bookings": completed_bookings,
    })


# ==========================================
# Bookings Page for User
# ==========================================

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        customer=request.user
    ).select_related("service", "provider").order_by("-date", "-start_time")

    return render(request, "bookings/my_bookings_user.html", {
        "bookings": bookings
    })

# ==========================================
# Cancel Booking
# ==========================================


@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking and free up the availability slot"""

    # Get the booking and ensure it belongs to the current user
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        customer=request.user
    )

    if request.method == "POST":
        from datetime import datetime, timedelta

        # Get the associated availability slot
        availability = booking.availability

        # Store booking details for the message
        service_name = booking.service.name
        booking_date = booking.date

        # Free up the availability slot
        if availability:
            availability.is_available = True
            availability.save()

            # Free up overlapping slots that were blocked by this booking
            booking_start = datetime.combine(booking.date, booking.start_time)
            booking_end = datetime.combine(booking.date, booking.end_time)

            # Find all unavailable slots for this service on the same date
            overlapping_slots = Availability.objects.filter(
                provider=booking.provider,
                service=booking.service,
                date=booking.date,
                is_available=False
            ).exclude(id=availability.id)

            # Check each slot to see if it was blocked by this booking
            for slot in overlapping_slots:
                slot_start = datetime.combine(booking.date, slot.start_time)
                slot_end_calc = slot_start + timedelta(minutes=booking.service.duration)

                # If this slot was overlapping with the cancelled booking
                if slot_start < booking_end and slot_end_calc > booking_start:
                    # Check if there are other active bookings blocking this slot
                    other_bookings = Booking.objects.filter(
                        provider=booking.provider,
                        date=booking.date,
                        status__in=['pending', 'confirmed']
                    ).exclude(id=booking.id)

                    slot_is_blocked = False
                    for other_booking in other_bookings:
                        other_start = datetime.combine(booking.date, other_booking.start_time)
                        other_end = datetime.combine(booking.date, other_booking.end_time)

                        if slot_start < other_end and slot_end_calc > other_start:
                            slot_is_blocked = True
                            break

                    # Only free the slot if no other bookings block it
                    if not slot_is_blocked:
                        slot.is_available = True
                        slot.save()

        # Delete the booking
        booking.delete()

        messages.success(
            request,
            f'Your booking for "{service_name}" on {booking_date} has been cancelled successfully.'
        )

        return redirect('my_bookings')

    # If GET request, redirect to bookings page
    return redirect('my_bookings')


@login_required
def delete_availability(request, availability_id):
    """Delete an availability slot - only if not booked and owned by provider"""

    # Get the availability slot
    availability = get_object_or_404(Availability, id=availability_id)

    # Security check: Only the provider who created it can delete
    if availability.provider != request.user:
        messages.error(request, "You don't have permission to delete this availability slot.")
        return redirect('add_availability')

    # Check if this slot is booked (has a related booking)
    has_booking = Booking.objects.filter(
        availability=availability,
        status__in=['pending', 'confirmed']
    ).exists()

    if has_booking:
        messages.error(
            request,
            "Cannot delete this slot - it has an active booking. Please cancel the booking first."
        )
        return redirect('add_availability')

    # Check if slot is already marked as unavailable (booked)
    if not availability.is_available:
        messages.warning(
            request,
            "This slot is already booked and cannot be deleted. Cancel the booking first."
        )
        return redirect('add_availability')

    # Store info for success message before deletion
    slot_date = availability.date.strftime('%B %d, %Y')
    slot_time = availability.start_time.strftime('%I:%M %p')
    service_name = availability.service.name if availability.service else "General availability"

    # Delete the availability slot
    availability.delete()

    messages.success(
        request,
        f'Availability slot for "{service_name}" on {slot_date} at {slot_time} has been deleted successfully.'
    )

    return redirect('add_availability')
