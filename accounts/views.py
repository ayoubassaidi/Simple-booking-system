from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserRegistrationForm, ProviderRegistrationForm

# Create your views here.


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
            return redirect('dashboard')
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
            return redirect('dashboard')
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
    except UserProfile.DoesNotExist:
        user_profile = None
        user_type = "User"

    # Prepare context data for the dashboard
    context = {
        'username': request.user.username,
        'user_type': user_type,
        'email': request.user.email if request.user.email else 'Not provided',
        'date_joined': request.user.date_joined,
        'last_login': request.user.last_login,
        'user_profile': user_profile,  # Pass the entire profile for template access
    }

    return render(request, 'accounts/dashboard.html', context)
