# bookings/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from accounts.models import UserProfile
from .models import Availability, Provider, Service, SearchQuery
from .forms import ServiceForm


@login_required
def add_availability(request):
    # Ensure only providers can access
    profile = UserProfile.objects.get(user=request.user)
    if profile.user_type != "provider":
        return redirect("dashboard")

    # Get provider's services for the dropdown
    provider_services = Service.objects.filter(provider=request.user, is_active=True)

    if request.method == "POST":
        service_id = request.POST.get("service")
        service = None

        if service_id:
            service = Service.objects.get(id=service_id, provider=request.user)

        Availability.objects.create(
            provider=request.user,
            service=service,
            date=request.POST.get("date"),
            start_time=request.POST.get("start_time"),
            end_time=request.POST.get("end_time"),
        )
        messages.success(request, "Availability slot added successfully!")
        return redirect("add_availability")

    slots = Availability.objects.filter(provider=request.user).select_related('service').order_by("date", "start_time")

    return render(request, "bookings/add_availability.html", {
        "slots": slots,
        "provider_services": provider_services,
    })


# Browse Service Providers - Shows all active services
def browse_providers(request):
    # Start with all active services
    services = Service.objects.filter(is_active=True).select_related('provider')

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
# ==========================================
# SERVICE MANAGEMENT VIEWS (Providers Only)
# ==========================================

@login_required
def my_services(request):
    """List all services for the logged-in provider"""
    # Ensure only providers can access
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.user_type != 'provider':
            messages.error(request, 'Only service providers can manage services.')
            return redirect('dashboard')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
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
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.user_type != 'provider':
            messages.error(request, 'Only service providers can add services.')
            return redirect('dashboard')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user
            service.save()
            messages.success(request, f'Service "{service.name}" added successfully!')
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
            messages.success(request, f'Service "{service.name}" updated successfully!')
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
        messages.success(request, f'Service "{service_name}" deleted successfully!')
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
    messages.success(request, f'Service "{service.name}" {status_text} successfully!')

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
    services = Service.objects.filter(is_active=True).select_related('provider')

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

def view_availability(request, service_id):
    """View availability calendar for a specific service"""
    from datetime import datetime, timedelta

    service = get_object_or_404(Service, id=service_id, is_active=True)

    # Get the selected date from query params or default to today
    selected_date_str = request.GET.get('date')
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = datetime.now().date()
    else:
        selected_date = datetime.now().date()

    # Generate 7 days starting from today
    today = datetime.now().date()
    week_dates = []
    for i in range(7):
        date = today + timedelta(days=i)
        week_dates.append({
            'date': date,
            'day_name': date.strftime('%a'),
            'day_num': date.strftime('%d'),
            'is_selected': date == selected_date
        })

    # Get availability slots for the selected date
    availability_slots = Availability.objects.filter(
        provider=service.provider,
        service=service,
        date=selected_date
    ).order_by('start_time')

    # Generate time slots for the day (9 AM to 6 PM in 1-hour intervals)
    time_slots = []
    for hour in range(9, 18):
        time_obj = datetime.strptime(f'{hour:02d}:00', '%H:%M').time()

        # Check if this time slot is available
        is_available = availability_slots.filter(
            start_time__lte=time_obj,
            end_time__gt=time_obj,
            is_available=True
        ).exists()

        # Format time for display
        display_time = datetime.strptime(f'{hour:02d}:00', '%H:%M').strftime('%I:%M %p')

        time_slots.append({
            'time': time_obj.strftime('%H:%M'),
            'display_time': display_time,
            'is_available': is_available
        })

    context = {
        'service': service,
        'week_dates': week_dates,
        'time_slots': time_slots,
        'selected_date': selected_date,
    }

    return render(request, 'bookings/view_availability.html', context)
