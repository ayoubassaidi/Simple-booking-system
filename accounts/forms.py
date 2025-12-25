from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    """Extended registration form for regular users"""
    email = forms.EmailField(
        required=True,
        help_text="Enter a valid email address"
    )
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        help_text="Your contact phone number"
    )
    birthday = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Your date of birth"
    )
    address = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Street, City, Postal Code'}),
        help_text="Your full address"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProviderRegistrationForm(UserCreationForm):
    """Extended registration form for service providers"""
    email = forms.EmailField(
        required=True,
        help_text="Enter a valid email address"
    )
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        help_text="Your contact phone number"
    )
    city = forms.CharField(
        max_length=100,
        required=True,
        help_text="City where you provide services"
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about your services and experience...'}),
        required=True,
        help_text="Brief description of your services"
    )
    service_type = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'e.g., Plumbing, Cleaning, Photography'}),
        help_text="What kind of service do you provide?"
    )
    kvk_number = forms.CharField(
        max_length=20,
        required=True,
        help_text="KVK (Chamber of Commerce) number"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
