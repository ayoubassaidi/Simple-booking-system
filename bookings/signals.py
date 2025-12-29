from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import UserProfile
from .models import ProviderProfile


@receiver(post_save, sender=UserProfile)
def create_provider_profile(sender, instance, created, **kwargs):
    """
    Automatically create ProviderProfile when UserProfile is created with user_type='provider'
    or when user_type is changed to 'provider'
    """
    if instance.user_type == 'provider':
        # Check if ProviderProfile already exists
        if not hasattr(instance.user, 'provider_profile'):
            # Create ProviderProfile from UserProfile data
            ProviderProfile.objects.create(
                user=instance.user,
                service_type=instance.service_type or 'other',
                bio=instance.bio or f"Services provided by {instance.user.username}",
                city=instance.city or 'Not specified',
                phone_number=instance.phone_number or '',
                kvk_number=instance.kvk_number or '',
                years_experience=0,
                rating=0.0,
                total_bookings=0,
                is_verified=False,
                is_active=True,
            )
        else:
            # Update existing ProviderProfile with UserProfile data
            provider_profile = instance.user.provider_profile
            provider_profile.service_type = instance.service_type or provider_profile.service_type
            provider_profile.bio = instance.bio or provider_profile.bio
            provider_profile.city = instance.city or provider_profile.city
            provider_profile.phone_number = instance.phone_number or provider_profile.phone_number
            provider_profile.kvk_number = instance.kvk_number or provider_profile.kvk_number
            provider_profile.save()


@receiver(post_save, sender=UserProfile)
def delete_provider_profile_if_not_provider(sender, instance, **kwargs):
    """
    Delete ProviderProfile if user_type is changed from 'provider' to something else
    """
    if instance.user_type != 'provider':
        try:
            if hasattr(instance.user, 'provider_profile'):
                instance.user.provider_profile.delete()
        except ProviderProfile.DoesNotExist:
            pass
