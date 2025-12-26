from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q
from .models import UserProfile
from .forms import UserRegistrationForm, ProviderRegistrationForm
from bookings.models import Notification, Service, Booking
from datetime import datetime, timedelta
import random

# Create your views here.


def home(request):
    """Home/landing page with featured services and categories"""
    # Get 6 random featured services
    all_services = list(Service.objects.filter(is_active=True).select_related('provider'))
    featured_services = random.sample(all_services, min(6, len(all_services)))

    # Get popular categories with service counts
    category_stats = Service.objects.filter(is_active=True).values('category').annotate(
        count=Count('id')
    ).order_by('-count')[:6]

    # Get category display names
    category_dict = dict(Service.CATEGORY_CHOICES)
    popular_categories = [
        {
            'value': cat['category'],
            'label': category_dict.get(cat['category'], cat['category']),
            'count': cat['count']
        }
        for cat in category_stats
    ]

    context = {
        'featured_services': featured_services,
        'popular_categories': popular_categories,
    }

    return render(request, 'home.html', context)


def custom_login(request):
    """Custom login view with account type validation"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        account_type = request.POST.get('account_type', 'user')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if user has a profile
            try:
                user_profile = UserProfile.objects.get(user=user)

                # Validate account type matches
                if user_profile.user_type != account_type:
                    # Wrong account type selected
                    if account_type == 'user':
                        messages.error(request, 'You are not allowed to login with this panel. This account is registered as a Service Provider. Please select "Provider" to login.')
                    else:
                        messages.error(request, 'You are not allowed to login with this panel. This account is registered as a User. Please select "User" to login.')
                    return redirect('login')

                # Account type matches - login successful
                login(request, user)
                return redirect('dashboard')

            except UserProfile.DoesNotExist:
                # No profile found - allow login anyway
                login(request, user)
                return redirect('dashboard')
        else:
            # Invalid credentials
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login.html')


def index(request):
    """Landing page where users choose their account type"""
    return render(request, 'accounts/index.html')


def register_user(request):
    """Registration page for regular users"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save()

            # Create user profile with additional data
            UserProfile.objects.create(
                user=user,
                user_type='user',
                phone_number=form.cleaned_data.get('phone_number'),
                birthday=form.cleaned_data.get('birthday'),
                address=form.cleaned_data.get('address')
            )

            # Log the user in
            login(request, user)
            return redirect('success')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {
        'form': form,
        'user_type': 'User',
        'icon': 'person'
    })


def register_provider(request):
    """Registration page for service providers"""
    if request.method == 'POST':
        form = ProviderRegistrationForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save()

            # Create provider profile with additional data
            UserProfile.objects.create(
                user=user,
                user_type='provider',
                phone_number=form.cleaned_data.get('phone_number'),
                city=form.cleaned_data.get('city'),
                bio=form.cleaned_data.get('bio'),
                service_type=form.cleaned_data.get('service_type'),
                kvk_number=form.cleaned_data.get('kvk_number')
            )

            # Log the user in
            login(request, user)
            return redirect('success')
    else:
        form = ProviderRegistrationForm()

    return render(request, 'accounts/register.html', {
        'form': form,
        'user_type': 'Service Provider',
        'icon': 'briefcase'
    })


def success(request):
    """Success page after registration"""
    return render(request, 'accounts/success.html')


@login_required
def dashboard(request):
    """User dashboard - only accessible when logged in"""
    # Get the user's profile to display user type
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        user_type = user_profile.get_user_type_display()
        is_provider = user_profile.user_type == 'provider'
    except UserProfile.DoesNotExist:
        user_profile = None
        user_type = "User"
        is_provider = False

    # Initialize context
    context = {
        'username': request.user.username,
        'user_type': user_type,
        'email': request.user.email if request.user.email else 'Not provided',
        'date_joined': request.user.date_joined,
        'last_login': request.user.last_login,
        'user_profile': user_profile,
        'is_provider': is_provider,
    }

    # Provider Dashboard Statistics
    if is_provider:
        # Get all bookings where this user is the provider
        provider_bookings = Booking.objects.filter(provider=request.user)

        # Total bookings count
        total_bookings = provider_bookings.count()

        # Total money collected (from completed bookings)
        total_revenue = provider_bookings.filter(
            status='completed'
        ).aggregate(total=Sum('price'))['total'] or 0

        # Pending bookings
        pending_bookings = provider_bookings.filter(status='pending').count()

        # Completed bookings
        completed_bookings = provider_bookings.filter(status='completed').count()

        # Upcoming bookings (confirmed or pending, date in future)
        today = datetime.now().date()
        upcoming_bookings = provider_bookings.filter(
            Q(status='confirmed') | Q(status='pending'),
            date__gte=today
        ).order_by('date', 'start_time')[:5]

        # Recent bookings
        recent_bookings = provider_bookings.order_by('-created_at')[:5]

        # Active services count
        active_services = Service.objects.filter(provider=request.user, is_active=True).count()

        # This month's revenue
        first_day_of_month = datetime.now().replace(day=1).date()
        month_revenue = provider_bookings.filter(
            status='completed',
            date__gte=first_day_of_month
        ).aggregate(total=Sum('price'))['total'] or 0

        # Calculate total hours booked
        total_hours = 0
        for booking in provider_bookings.filter(Q(status='completed') | Q(status='confirmed')):
            start_datetime = datetime.combine(booking.date, booking.start_time)
            end_datetime = datetime.combine(booking.date, booking.end_time)
            duration = (end_datetime - start_datetime).total_seconds() / 3600
            total_hours += duration

        context.update({
            'total_bookings': total_bookings,
            'total_revenue': total_revenue,
            'pending_bookings': pending_bookings,
            'completed_bookings': completed_bookings,
            'upcoming_bookings': upcoming_bookings,
            'recent_bookings': recent_bookings,
            'active_services': active_services,
            'month_revenue': month_revenue,
            'total_hours': round(total_hours, 1),
        })

    # User (Customer) Dashboard Statistics
    else:
        # Get all bookings where this user is the customer
        customer_bookings = Booking.objects.filter(customer=request.user)

        # Total bookings count
        total_bookings = customer_bookings.count()

        # Upcoming bookings
        today = datetime.now().date()
        upcoming_bookings = customer_bookings.filter(
            Q(status='confirmed') | Q(status='pending'),
            date__gte=today
        ).order_by('date', 'start_time')[:5]

        # Past bookings
        past_bookings = customer_bookings.filter(
            date__lt=today
        ).order_by('-date', '-start_time')[:5]

        # Last completed booking
        last_booking = customer_bookings.filter(
            status='completed'
        ).order_by('-date', '-start_time').first()

        # Completed bookings count
        completed_bookings = customer_bookings.filter(status='completed').count()

        # Pending bookings count
        pending_bookings = customer_bookings.filter(status='pending').count()

        # Total money spent
        total_spent = customer_bookings.filter(
            status='completed'
        ).aggregate(total=Sum('price'))['total'] or 0

        # Calculate total hours booked
        total_hours = 0
        for booking in customer_bookings.filter(Q(status='completed') | Q(status='confirmed')):
            start_datetime = datetime.combine(booking.date, booking.start_time)
            end_datetime = datetime.combine(booking.date, booking.end_time)
            duration = (end_datetime - start_datetime).total_seconds() / 3600
            total_hours += duration

        context.update({
            'total_bookings': total_bookings,
            'upcoming_bookings': upcoming_bookings,
            'past_bookings': past_bookings,
            'last_booking': last_booking,
            'completed_bookings': completed_bookings,
            'pending_bookings': pending_bookings,
            'total_spent': total_spent,
            'total_hours': round(total_hours, 1),
        })

    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile(request):
    """User profile page"""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        # Update user information
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()

        # Update profile information
        if user_profile:
            user_profile.phone_number = request.POST.get('phone_number', '')

            if user_profile.user_type == 'user':
                user_profile.birthday = request.POST.get('birthday') or None
                user_profile.address = request.POST.get('address', '')
            else:  # provider
                user_profile.city = request.POST.get('city', '')
                user_profile.bio = request.POST.get('bio', '')
                user_profile.service_type = request.POST.get('service_type', '')
                user_profile.kvk_number = request.POST.get('kvk_number', '')

            user_profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def notifications(request):
    """Notifications page"""
    # Get all notifications for the user
    user_notifications = Notification.objects.filter(user=request.user)

    # Mark as read if action requested
    if request.GET.get('mark_read'):
        notification_id = request.GET.get('mark_read')
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            return redirect('notifications')
        except Notification.DoesNotExist:
            pass

    # Mark all as read
    if request.GET.get('mark_all_read') == 'true':
        user_notifications.update(is_read=True)
        messages.success(request, 'All notifications marked as read!')
        return redirect('notifications')

    # Delete notification
    if request.GET.get('delete'):
        notification_id = request.GET.get('delete')
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.delete()
            messages.success(request, 'Notification deleted!')
            return redirect('notifications')
        except Notification.DoesNotExist:
            pass

    # Statistics
    unread_count = user_notifications.filter(is_read=False).count()
    total_count = user_notifications.count()

    context = {
        'notifications': user_notifications,
        'unread_count': unread_count,
        'total_count': total_count,
    }

    return render(request, 'accounts/notifications.html', context)
