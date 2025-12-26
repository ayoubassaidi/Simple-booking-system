# Simple Django Management Command to Add Mock Providers
from django.core.management.base import BaseCommand
from bookings.models import Provider


class Command(BaseCommand):
    help = 'Add mock service providers to database'

    def handle(self, *args, **kwargs):
        # Clear existing providers
        Provider.objects.all().delete()

        # Mock Provider 1 - Jake's Plumbing
        Provider.objects.create(
            name="Jake's Plumbing",
            service_type='plumbing',
            location='amsterdam',
            rating=4.8,
            years_experience=5,
            completed_jobs=120,
            description="A desendentiel plumber, handout capritism. Gascad bapponing duueccetenced cogators in Amsterdam.",
            image_url="https://ui-avatars.com/api/?name=Jake&background=667eea&color=fff&size=200"
        )

        # Mock Provider 2 - Laura's Salon
        Provider.objects.create(
            name="Laura's Salon",
            service_type='salon',
            location='rotterdam',
            rating=4.9,
            years_experience=8,
            completed_jobs=300,
            description="Eqpey copIiare to ookyling with wrodessiewes hoibe ouembenies cureatected noti bants in notilication.",
            image_url="https://ui-avatars.com/api/?name=Laura&background=f093fb&color=fff&size=200"
        )

        # Mock Provider 3 - Mike's Therapy
        Provider.objects.create(
            name="Mike's Therapy",
            service_type='therapy',
            location='rotterdam',
            rating=4.7,
            years_experience=10,
            completed_jobs=250,
            description="Hiacgy captiare to nape profiersented porfessional therapy services in Rottiroziant Ltors receriency.",
            image_url="https://ui-avatars.com/api/?name=Mike&background=4facfe&color=fff&size=200"
        )

        # Mock Provider 4 - Anna's Cleaning
        Provider.objects.create(
            name="Anna's Cleaning",
            service_type='cleaning',
            location='utrecht',
            rating=4.6,
            years_experience=3,
            completed_jobs=80,
            description="Professional cleaning services for homes and offices. Reliable, thorough, and eco-friendly cleaning solutions.",
            image_url="https://ui-avatars.com/api/?name=Anna&background=28a745&color=fff&size=200"
        )

        self.stdout.write(self.style.SUCCESS('Successfully added 4 mock providers!'))
