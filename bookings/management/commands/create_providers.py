from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
from bookings.models import Service
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Create 30 service providers with their services'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating 30 service providers with services...')

        # Provider data with realistic information
        providers_data = [
            {
                'username': 'sarah_hair_studio',
                'email': 'sarah@hairstudio.com',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'city': 'Amsterdam',
                'bio': 'Professional hair stylist with 10 years of experience. Specialized in modern cuts and coloring techniques.',
                'service_type': 'Hair Styling',
                'kvk': '12345678',
                'services': [
                    {'name': 'Women Haircut & Style', 'category': 'salon_beauty', 'price': '45.00', 'duration': 60, 'description': 'Professional haircut with styling and blow-dry'},
                    {'name': 'Hair Coloring', 'category': 'salon_beauty', 'price': '85.00', 'duration': 120, 'description': 'Full color treatment with premium products'},
                    {'name': 'Balayage Highlights', 'category': 'salon_beauty', 'price': '120.00', 'duration': 180, 'description': 'Natural-looking highlights using balayage technique'},
                ]
            },
            {
                'username': 'mike_plumbing_pro',
                'email': 'mike@plumbingpro.nl',
                'first_name': 'Mike',
                'last_name': 'van der Berg',
                'city': 'Rotterdam',
                'bio': 'Licensed plumber with 15 years experience. Available for emergencies and regular maintenance.',
                'service_type': 'Plumbing',
                'kvk': '23456789',
                'services': [
                    {'name': 'Emergency Plumbing Repair', 'category': 'home_services', 'price': '95.00', 'duration': 120, 'description': '24/7 emergency plumbing service'},
                    {'name': 'Bathroom Installation', 'category': 'home_services', 'price': '450.00', 'duration': 240, 'description': 'Complete bathroom fitting and installation'},
                    {'name': 'Leak Detection & Repair', 'category': 'home_services', 'price': '75.00', 'duration': 90, 'description': 'Professional leak detection and repair service'},
                ]
            },
            {
                'username': 'lisa_yoga_wellness',
                'email': 'lisa@yogawellness.nl',
                'first_name': 'Lisa',
                'last_name': 'Vermeulen',
                'city': 'Utrecht',
                'bio': 'Certified yoga instructor and wellness coach. Helping people find balance and inner peace.',
                'service_type': 'Yoga & Wellness',
                'kvk': '34567890',
                'services': [
                    {'name': 'Private Yoga Session', 'category': 'health_wellness', 'price': '55.00', 'duration': 60, 'description': 'One-on-one personalized yoga instruction'},
                    {'name': 'Meditation Class', 'category': 'health_wellness', 'price': '35.00', 'duration': 60, 'description': 'Guided meditation for stress relief'},
                    {'name': 'Wellness Consultation', 'category': 'health_wellness', 'price': '65.00', 'duration': 90, 'description': 'Holistic wellness assessment and planning'},
                ]
            },
            {
                'username': 'tom_personal_trainer',
                'email': 'tom@fitcoach.nl',
                'first_name': 'Tom',
                'last_name': 'Bakker',
                'city': 'Amsterdam',
                'bio': 'Certified personal trainer specializing in weight loss and muscle building programs.',
                'service_type': 'Personal Training',
                'kvk': '45678901',
                'services': [
                    {'name': 'Personal Training Session', 'category': 'fitness', 'price': '60.00', 'duration': 60, 'description': 'Customized one-on-one training session'},
                    {'name': 'Nutrition Coaching', 'category': 'fitness', 'price': '50.00', 'duration': 60, 'description': 'Personalized nutrition plan and guidance'},
                    {'name': 'Fitness Assessment', 'category': 'fitness', 'price': '45.00', 'duration': 60, 'description': 'Complete fitness evaluation and goal setting'},
                ]
            },
            {
                'username': 'emma_massage_therapy',
                'email': 'emma@massagetherapy.nl',
                'first_name': 'Emma',
                'last_name': 'de Vries',
                'city': 'Amsterdam',
                'bio': 'Licensed massage therapist specializing in deep tissue and sports massage.',
                'service_type': 'Massage Therapy',
                'kvk': '56789012',
                'services': [
                    {'name': 'Deep Tissue Massage', 'category': 'health_wellness', 'price': '70.00', 'duration': 60, 'description': 'Therapeutic deep tissue massage'},
                    {'name': 'Sports Massage', 'category': 'health_wellness', 'price': '75.00', 'duration': 60, 'description': 'Specialized massage for athletes'},
                    {'name': 'Relaxation Massage', 'category': 'health_wellness', 'price': '65.00', 'duration': 90, 'description': 'Full body relaxation massage'},
                ]
            },
            {
                'username': 'david_math_tutor',
                'email': 'david@mathtutor.nl',
                'first_name': 'David',
                'last_name': 'Jansen',
                'city': 'Utrecht',
                'bio': 'Mathematics teacher with PhD. Tutoring high school and university students.',
                'service_type': 'Mathematics Tutoring',
                'kvk': '67890123',
                'services': [
                    {'name': 'High School Math Tutoring', 'category': 'education', 'price': '40.00', 'duration': 60, 'description': 'One-on-one math tutoring for high school'},
                    {'name': 'University Math Help', 'category': 'education', 'price': '55.00', 'duration': 60, 'description': 'Advanced mathematics tutoring'},
                    {'name': 'Exam Preparation', 'category': 'education', 'price': '65.00', 'duration': 90, 'description': 'Intensive exam preparation sessions'},
                ]
            },
            {
                'username': 'anna_cleaning_service',
                'email': 'anna@cleaningservice.nl',
                'first_name': 'Anna',
                'last_name': 'Smit',
                'city': 'Rotterdam',
                'bio': 'Professional cleaning service with eco-friendly products. Reliable and thorough.',
                'service_type': 'House Cleaning',
                'kvk': '78901234',
                'services': [
                    {'name': 'Regular House Cleaning', 'category': 'home_services', 'price': '35.00', 'duration': 120, 'description': 'Standard house cleaning service'},
                    {'name': 'Deep Cleaning', 'category': 'home_services', 'price': '55.00', 'duration': 180, 'description': 'Thorough deep cleaning service'},
                    {'name': 'Move-out Cleaning', 'category': 'home_services', 'price': '85.00', 'duration': 240, 'description': 'Complete move-out cleaning'},
                ]
            },
            {
                'username': 'peter_guitar_lessons',
                'email': 'peter@guitarlessons.nl',
                'first_name': 'Peter',
                'last_name': 'Hendriks',
                'city': 'Amsterdam',
                'bio': 'Professional guitarist with 20 years of teaching experience. All skill levels welcome.',
                'service_type': 'Music Lessons',
                'kvk': '89012345',
                'services': [
                    {'name': 'Beginner Guitar Lessons', 'category': 'education', 'price': '35.00', 'duration': 60, 'description': 'Guitar lessons for beginners'},
                    {'name': 'Advanced Guitar Coaching', 'category': 'education', 'price': '50.00', 'duration': 60, 'description': 'Advanced techniques and theory'},
                    {'name': 'Music Theory Class', 'category': 'education', 'price': '40.00', 'duration': 60, 'description': 'Music theory for guitarists'},
                ]
            },
            {
                'username': 'maria_nail_artist',
                'email': 'maria@nailart.nl',
                'first_name': 'Maria',
                'last_name': 'Rodriguez',
                'city': 'Amsterdam',
                'bio': 'Creative nail artist specializing in gel nails and nail art designs.',
                'service_type': 'Nail Art',
                'kvk': '90123456',
                'services': [
                    {'name': 'Gel Manicure', 'category': 'salon_beauty', 'price': '35.00', 'duration': 60, 'description': 'Long-lasting gel manicure'},
                    {'name': 'Nail Art Design', 'category': 'salon_beauty', 'price': '45.00', 'duration': 90, 'description': 'Custom nail art designs'},
                    {'name': 'Pedicure', 'category': 'salon_beauty', 'price': '40.00', 'duration': 60, 'description': 'Professional pedicure service'},
                ]
            },
            {
                'username': 'john_electrician',
                'email': 'john@electrician.nl',
                'first_name': 'John',
                'last_name': 'Peterson',
                'city': 'Rotterdam',
                'bio': 'Certified electrician for residential and commercial properties. Safe and reliable.',
                'service_type': 'Electrical Services',
                'kvk': '01234567',
                'services': [
                    {'name': 'Electrical Inspection', 'category': 'home_services', 'price': '65.00', 'duration': 60, 'description': 'Complete electrical safety inspection'},
                    {'name': 'Lighting Installation', 'category': 'home_services', 'price': '55.00', 'duration': 90, 'description': 'Professional lighting installation'},
                    {'name': 'Emergency Electrical Repair', 'category': 'home_services', 'price': '95.00', 'duration': 60, 'description': 'Emergency electrical services'},
                ]
            },
            {
                'username': 'sophie_photographer',
                'email': 'sophie@photography.nl',
                'first_name': 'Sophie',
                'last_name': 'Williams',
                'city': 'Utrecht',
                'bio': 'Professional photographer specializing in portraits and events.',
                'service_type': 'Photography',
                'kvk': '11234568',
                'services': [
                    {'name': 'Portrait Photography', 'category': 'other', 'price': '120.00', 'duration': 120, 'description': 'Professional portrait photo session'},
                    {'name': 'Event Photography', 'category': 'other', 'price': '250.00', 'duration': 240, 'description': 'Complete event coverage'},
                    {'name': 'Photo Editing Service', 'category': 'other', 'price': '45.00', 'duration': 60, 'description': 'Professional photo retouching'},
                ]
            },
            {
                'username': 'alex_web_developer',
                'email': 'alex@webdev.nl',
                'first_name': 'Alex',
                'last_name': 'Chen',
                'city': 'Amsterdam',
                'bio': 'Full-stack web developer with expertise in modern frameworks and technologies.',
                'service_type': 'Web Development',
                'kvk': '22345679',
                'services': [
                    {'name': 'Website Development', 'category': 'technology', 'price': '500.00', 'duration': 240, 'description': 'Custom website development'},
                    {'name': 'Website Maintenance', 'category': 'technology', 'price': '75.00', 'duration': 60, 'description': 'Monthly website maintenance'},
                    {'name': 'SEO Optimization', 'category': 'technology', 'price': '150.00', 'duration': 120, 'description': 'Search engine optimization service'},
                ]
            },
            {
                'username': 'rachel_makeup_artist',
                'email': 'rachel@makeup.nl',
                'first_name': 'Rachel',
                'last_name': 'Taylor',
                'city': 'Amsterdam',
                'bio': 'Professional makeup artist for weddings, events, and photoshoots.',
                'service_type': 'Makeup Artistry',
                'kvk': '33456780',
                'services': [
                    {'name': 'Bridal Makeup', 'category': 'salon_beauty', 'price': '120.00', 'duration': 120, 'description': 'Complete bridal makeup service'},
                    {'name': 'Event Makeup', 'category': 'salon_beauty', 'price': '75.00', 'duration': 60, 'description': 'Professional makeup for events'},
                    {'name': 'Makeup Lesson', 'category': 'salon_beauty', 'price': '85.00', 'duration': 90, 'description': 'Personal makeup tutorial'},
                ]
            },
            {
                'username': 'mark_landscaping',
                'email': 'mark@landscaping.nl',
                'first_name': 'Mark',
                'last_name': 'van Dijk',
                'city': 'Rotterdam',
                'bio': 'Professional landscaping and garden maintenance services.',
                'service_type': 'Landscaping',
                'kvk': '44567891',
                'services': [
                    {'name': 'Garden Design', 'category': 'home_services', 'price': '150.00', 'duration': 120, 'description': 'Custom garden design consultation'},
                    {'name': 'Lawn Maintenance', 'category': 'home_services', 'price': '45.00', 'duration': 60, 'description': 'Regular lawn care service'},
                    {'name': 'Tree Pruning', 'category': 'home_services', 'price': '85.00', 'duration': 120, 'description': 'Professional tree pruning'},
                ]
            },
            {
                'username': 'julia_piano_teacher',
                'email': 'julia@piano.nl',
                'first_name': 'Julia',
                'last_name': 'Mueller',
                'city': 'Utrecht',
                'bio': 'Classically trained pianist offering lessons for all ages and skill levels.',
                'service_type': 'Piano Lessons',
                'kvk': '55678902',
                'services': [
                    {'name': 'Piano Lessons - Beginner', 'category': 'education', 'price': '40.00', 'duration': 60, 'description': 'Piano lessons for beginners'},
                    {'name': 'Piano Lessons - Advanced', 'category': 'education', 'price': '55.00', 'duration': 60, 'description': 'Advanced piano instruction'},
                    {'name': 'Music Theory for Piano', 'category': 'education', 'price': '45.00', 'duration': 60, 'description': 'Theory lessons for pianists'},
                ]
            },
            {
                'username': 'chris_car_mechanic',
                'email': 'chris@carmechanic.nl',
                'first_name': 'Chris',
                'last_name': 'Anderson',
                'city': 'Amsterdam',
                'bio': 'Experienced car mechanic specializing in maintenance and repairs.',
                'service_type': 'Auto Repair',
                'kvk': '66789013',
                'services': [
                    {'name': 'Car Maintenance Check', 'category': 'other', 'price': '55.00', 'duration': 60, 'description': 'Complete vehicle inspection'},
                    {'name': 'Oil Change Service', 'category': 'other', 'price': '45.00', 'duration': 60, 'description': 'Professional oil change'},
                    {'name': 'Brake Repair', 'category': 'other', 'price': '95.00', 'duration': 120, 'description': 'Brake system repair and replacement'},
                ]
            },
            {
                'username': 'nina_interior_designer',
                'email': 'nina@interior.nl',
                'first_name': 'Nina',
                'last_name': 'Kowalski',
                'city': 'Amsterdam',
                'bio': 'Interior designer creating beautiful and functional living spaces.',
                'service_type': 'Interior Design',
                'kvk': '77890124',
                'services': [
                    {'name': 'Interior Design Consultation', 'category': 'business', 'price': '100.00', 'duration': 120, 'description': 'Professional interior design advice'},
                    {'name': 'Room Makeover', 'category': 'business', 'price': '350.00', 'duration': 240, 'description': 'Complete room transformation'},
                    {'name': 'Color Consultation', 'category': 'business', 'price': '65.00', 'duration': 60, 'description': 'Professional color scheme advice'},
                ]
            },
            {
                'username': 'robert_accountant',
                'email': 'robert@accounting.nl',
                'first_name': 'Robert',
                'last_name': 'Visser',
                'city': 'Rotterdam',
                'bio': 'Certified accountant helping businesses and individuals with tax and financial planning.',
                'service_type': 'Accounting',
                'kvk': '88901235',
                'services': [
                    {'name': 'Tax Preparation', 'category': 'business', 'price': '120.00', 'duration': 120, 'description': 'Personal and business tax filing'},
                    {'name': 'Financial Consultation', 'category': 'business', 'price': '85.00', 'duration': 60, 'description': 'Financial planning advice'},
                    {'name': 'Bookkeeping Service', 'category': 'business', 'price': '65.00', 'duration': 60, 'description': 'Monthly bookkeeping service'},
                ]
            },
            {
                'username': 'laura_nutritionist',
                'email': 'laura@nutrition.nl',
                'first_name': 'Laura',
                'last_name': 'Schmidt',
                'city': 'Utrecht',
                'bio': 'Registered nutritionist helping people achieve their health goals through proper nutrition.',
                'service_type': 'Nutrition Counseling',
                'kvk': '99012346',
                'services': [
                    {'name': 'Nutrition Consultation', 'category': 'health_wellness', 'price': '70.00', 'duration': 60, 'description': 'Personalized nutrition assessment'},
                    {'name': 'Meal Planning Service', 'category': 'health_wellness', 'price': '55.00', 'duration': 60, 'description': 'Custom meal plan creation'},
                    {'name': 'Weight Loss Coaching', 'category': 'health_wellness', 'price': '80.00', 'duration': 90, 'description': 'Comprehensive weight loss program'},
                ]
            },
            {
                'username': 'kevin_dog_trainer',
                'email': 'kevin@dogtraining.nl',
                'first_name': 'Kevin',
                'last_name': 'Brown',
                'city': 'Amsterdam',
                'bio': 'Professional dog trainer specializing in obedience and behavior modification.',
                'service_type': 'Dog Training',
                'kvk': '10123457',
                'services': [
                    {'name': 'Puppy Training', 'category': 'other', 'price': '55.00', 'duration': 60, 'description': 'Basic puppy obedience training'},
                    {'name': 'Behavior Modification', 'category': 'other', 'price': '75.00', 'duration': 90, 'description': 'Problem behavior correction'},
                    {'name': 'Advanced Obedience', 'category': 'other', 'price': '65.00', 'duration': 60, 'description': 'Advanced dog training'},
                ]
            },
            {
                'username': 'jessica_life_coach',
                'email': 'jessica@lifecoach.nl',
                'first_name': 'Jessica',
                'last_name': 'White',
                'city': 'Rotterdam',
                'bio': 'Certified life coach helping individuals achieve personal and professional goals.',
                'service_type': 'Life Coaching',
                'kvk': '21234568',
                'services': [
                    {'name': 'Life Coaching Session', 'category': 'business', 'price': '85.00', 'duration': 60, 'description': 'Personal development coaching'},
                    {'name': 'Career Coaching', 'category': 'business', 'price': '95.00', 'duration': 90, 'description': 'Professional career guidance'},
                    {'name': 'Goal Setting Workshop', 'category': 'business', 'price': '75.00', 'duration': 120, 'description': 'Goal achievement strategies'},
                ]
            },
            {
                'username': 'daniel_spanish_tutor',
                'email': 'daniel@spanish.nl',
                'first_name': 'Daniel',
                'last_name': 'Martinez',
                'city': 'Utrecht',
                'bio': 'Native Spanish speaker offering language lessons for all levels.',
                'service_type': 'Language Tutoring',
                'kvk': '32345679',
                'services': [
                    {'name': 'Spanish Lessons - Beginner', 'category': 'education', 'price': '35.00', 'duration': 60, 'description': 'Spanish for beginners'},
                    {'name': 'Spanish Conversation Practice', 'category': 'education', 'price': '40.00', 'duration': 60, 'description': 'Conversational Spanish practice'},
                    {'name': 'Business Spanish', 'category': 'education', 'price': '50.00', 'duration': 60, 'description': 'Spanish for business professionals'},
                ]
            },
            {
                'username': 'melissa_esthetician',
                'email': 'melissa@skincare.nl',
                'first_name': 'Melissa',
                'last_name': 'Davis',
                'city': 'Amsterdam',
                'bio': 'Licensed esthetician specializing in skincare treatments and facials.',
                'service_type': 'Skincare',
                'kvk': '43456780',
                'services': [
                    {'name': 'Deep Cleansing Facial', 'category': 'salon_beauty', 'price': '65.00', 'duration': 60, 'description': 'Professional facial treatment'},
                    {'name': 'Anti-Aging Treatment', 'category': 'salon_beauty', 'price': '85.00', 'duration': 90, 'description': 'Advanced anti-aging facial'},
                    {'name': 'Acne Treatment', 'category': 'salon_beauty', 'price': '70.00', 'duration': 60, 'description': 'Specialized acne treatment'},
                ]
            },
            {
                'username': 'brian_handyman',
                'email': 'brian@handyman.nl',
                'first_name': 'Brian',
                'last_name': 'Wilson',
                'city': 'Rotterdam',
                'bio': 'Experienced handyman for all types of home repairs and improvements.',
                'service_type': 'Handyman Services',
                'kvk': '54567891',
                'services': [
                    {'name': 'General Home Repairs', 'category': 'home_services', 'price': '45.00', 'duration': 60, 'description': 'Various home repair services'},
                    {'name': 'Furniture Assembly', 'category': 'home_services', 'price': '35.00', 'duration': 60, 'description': 'Professional furniture assembly'},
                    {'name': 'Painting Service', 'category': 'home_services', 'price': '50.00', 'duration': 120, 'description': 'Interior painting service'},
                ]
            },
            {
                'username': 'amanda_voice_coach',
                'email': 'amanda@voicecoach.nl',
                'first_name': 'Amanda',
                'last_name': 'Green',
                'city': 'Utrecht',
                'bio': 'Professional voice coach for singers and public speakers.',
                'service_type': 'Voice Coaching',
                'kvk': '65678902',
                'services': [
                    {'name': 'Vocal Training', 'category': 'education', 'price': '50.00', 'duration': 60, 'description': 'Professional voice training'},
                    {'name': 'Public Speaking Coach', 'category': 'education', 'price': '65.00', 'duration': 60, 'description': 'Public speaking improvement'},
                    {'name': 'Performance Preparation', 'category': 'education', 'price': '75.00', 'duration': 90, 'description': 'Performance coaching session'},
                ]
            },
            {
                'username': 'patrick_carpenter',
                'email': 'patrick@carpentry.nl',
                'first_name': 'Patrick',
                'last_name': 'Thompson',
                'city': 'Amsterdam',
                'bio': 'Master carpenter specializing in custom woodwork and furniture.',
                'service_type': 'Carpentry',
                'kvk': '76789013',
                'services': [
                    {'name': 'Custom Furniture Build', 'category': 'home_services', 'price': '350.00', 'duration': 240, 'description': 'Custom furniture creation'},
                    {'name': 'Cabinet Installation', 'category': 'home_services', 'price': '250.00', 'duration': 180, 'description': 'Professional cabinet fitting'},
                    {'name': 'Wood Repair Service', 'category': 'home_services', 'price': '55.00', 'duration': 60, 'description': 'Wooden furniture repair'},
                ]
            },
            {
                'username': 'nicole_pilates_instructor',
                'email': 'nicole@pilates.nl',
                'first_name': 'Nicole',
                'last_name': 'King',
                'city': 'Rotterdam',
                'bio': 'Certified Pilates instructor helping clients improve strength and flexibility.',
                'service_type': 'Pilates',
                'kvk': '87890124',
                'services': [
                    {'name': 'Private Pilates Session', 'category': 'fitness', 'price': '60.00', 'duration': 60, 'description': 'One-on-one Pilates training'},
                    {'name': 'Mat Pilates Class', 'category': 'fitness', 'price': '45.00', 'duration': 60, 'description': 'Group mat Pilates class'},
                    {'name': 'Reformer Pilates', 'category': 'fitness', 'price': '70.00', 'duration': 60, 'description': 'Reformer Pilates session'},
                ]
            },
            {
                'username': 'steven_it_support',
                'email': 'steven@itsupport.nl',
                'first_name': 'Steven',
                'last_name': 'Lee',
                'city': 'Utrecht',
                'bio': 'IT support specialist for home and small business computer problems.',
                'service_type': 'IT Support',
                'kvk': '98901235',
                'services': [
                    {'name': 'Computer Repair', 'category': 'technology', 'price': '55.00', 'duration': 60, 'description': 'Computer troubleshooting and repair'},
                    {'name': 'Network Setup', 'category': 'technology', 'price': '85.00', 'duration': 120, 'description': 'Home network installation'},
                    {'name': 'Virus Removal', 'category': 'technology', 'price': '45.00', 'duration': 60, 'description': 'Malware and virus removal'},
                ]
            },
            {
                'username': 'rebecca_event_planner',
                'email': 'rebecca@events.nl',
                'first_name': 'Rebecca',
                'last_name': 'Hall',
                'city': 'Amsterdam',
                'bio': 'Professional event planner creating memorable experiences for all occasions.',
                'service_type': 'Event Planning',
                'kvk': '09012346',
                'services': [
                    {'name': 'Event Planning Consultation', 'category': 'business', 'price': '95.00', 'duration': 120, 'description': 'Event planning and coordination'},
                    {'name': 'Wedding Planning', 'category': 'business', 'price': '500.00', 'duration': 240, 'description': 'Complete wedding planning service'},
                    {'name': 'Corporate Event Planning', 'category': 'business', 'price': '350.00', 'duration': 180, 'description': 'Business event coordination'},
                ]
            },
            {
                'username': 'gary_swim_instructor',
                'email': 'gary@swimming.nl',
                'first_name': 'Gary',
                'last_name': 'Adams',
                'city': 'Rotterdam',
                'bio': 'Certified swimming instructor for children and adults.',
                'service_type': 'Swimming Lessons',
                'kvk': '19123457',
                'services': [
                    {'name': 'Kids Swimming Lessons', 'category': 'fitness', 'price': '35.00', 'duration': 60, 'description': 'Swimming lessons for children'},
                    {'name': 'Adult Swimming Lessons', 'category': 'fitness', 'price': '40.00', 'duration': 60, 'description': 'Swimming lessons for adults'},
                    {'name': 'Advanced Swim Training', 'category': 'fitness', 'price': '50.00', 'duration': 60, 'description': 'Advanced swimming techniques'},
                ]
            },
        ]

        created_count = 0
        for provider_data in providers_data:
            try:
                # Check if user already exists
                if User.objects.filter(username=provider_data['username']).exists():
                    self.stdout.write(self.style.WARNING(f"User {provider_data['username']} already exists, skipping..."))
                    continue

                # Create user
                user = User.objects.create_user(
                    username=provider_data['username'],
                    email=provider_data['email'],
                    password='provider123',  # Default password for all providers
                    first_name=provider_data['first_name'],
                    last_name=provider_data['last_name']
                )

                # Create user profile
                UserProfile.objects.create(
                    user=user,
                    user_type='provider',
                    phone_number=f'+31 6 {random.randint(10000000, 99999999)}',
                    city=provider_data['city'],
                    bio=provider_data['bio'],
                    service_type=provider_data['service_type'],
                    kvk_number=provider_data['kvk']
                )

                # Create services
                for service_data in provider_data['services']:
                    Service.objects.create(
                        provider=user,
                        name=service_data['name'],
                        category=service_data['category'],
                        description=service_data['description'],
                        price=Decimal(service_data['price']),
                        duration=service_data['duration'],
                        is_active=True
                    )

                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created provider: {provider_data['username']} with {len(provider_data['services'])} services"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating {provider_data['username']}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {created_count} providers!'))
        self.stdout.write(self.style.SUCCESS('All providers have password: provider123'))
