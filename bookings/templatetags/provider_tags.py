from django import template
from bookings.models import ProviderProfile

register = template.Library()


@register.filter(name='is_provider')
def is_provider(user):
    """
    Template filter to check if a user is a provider
    Usage in template: {% if request.user|is_provider %}
    """
    return ProviderProfile.is_provider(user)


@register.simple_tag
def get_provider_profile(user):
    """
    Template tag to get the provider profile for a user
    Usage in template: {% get_provider_profile request.user as provider_profile %}
    """
    return ProviderProfile.get_provider_profile(user)
