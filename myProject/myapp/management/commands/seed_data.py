from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files import File
from datetime import timedelta
import os
from django.conf import settings
from myapp.models import (
    UserProfile, ModelCategory, Model, ModelBooking,
    MagazineCategory, Magazine, MagazineOrder,
    Photoshoot, Runway, Campaign
)

class Command(BaseCommand):
    help = 'Seeds the database with initial data for the modeling agency'

    def get_static_image_path(self, image_name):
        """Get the full path to a static image file"""
        return os.path.join(settings.STATIC_ROOT, 'images', image_name)

    def create_superuser(self):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))

    def seed_model_categories(self):
        categories = [
            {'name': 'High Fashion', 'description': 'Luxury and high-end fashion modeling'},
            {'name': 'Editorial', 'description': 'Magazine and editorial modeling'},
            {'name': 'Runway', 'description': 'Fashion show and runway modeling'},
            {'name': 'Commercial', 'description': 'Commercial and advertising modeling'},
            {'name': 'Beauty', 'description': 'Beauty and cosmetics modeling'},
            {'name': 'Luxury', 'description': 'Luxury brand and high-end modeling'},
        ]
        
        for category in categories:
            ModelCategory.objects.get_or_create(
                name=category['name'],
                defaults={'description': category['description']}
            )
        self.stdout.write(self.style.SUCCESS('Model categories created successfully'))

    def seed_magazine_categories(self):
        categories = [
            {'name': 'Fashion', 'description': 'Fashion magazines and editorials'},
            {'name': 'Beauty', 'description': 'Beauty and cosmetics magazines'},
            {'name': 'Lifestyle', 'description': 'Lifestyle and culture magazines'},
        ]
        
        for category in categories:
            MagazineCategory.objects.get_or_create(
                name=category['name'],
                defaults={'description': category['description']}
            )
        self.stdout.write(self.style.SUCCESS('Magazine categories created successfully'))

    def seed_models(self):
        models_data = [
            {
                'username': 'anok_yai',
                'email': 'anok@example.com',
                'password': 'model123',
                'first_name': 'Anok',
                'last_name': 'Yai',
                'gender': 'F',
                'age': 25,
                'height': 178,  # 5'10"
                'measurements': '34-24-34',
                'category': 'High Fashion',
                'portfolio_link': 'https://example.com/anok',
                'image': 'model_anok.avif'
            },
            {
                'username': 'bella_hadid',
                'email': 'bella@example.com',
                'password': 'model123',
                'first_name': 'Bella',
                'last_name': 'Hadid',
                'gender': 'F',
                'age': 27,
                'height': 175,  # 5'9"
                'measurements': '32-23-35',
                'category': 'Runway',
                'portfolio_link': 'https://example.com/bella',
                'image': 'model_bella.jpg'
            },
            {
                'username': 'kendall_jenner',
                'email': 'kendall@example.com',
                'password': 'model123',
                'first_name': 'Kendall',
                'last_name': 'Jenner',
                'gender': 'F',
                'age': 28,
                'height': 180,  # 5'11"
                'measurements': '34-25-36',
                'category': 'Commercial',
                'portfolio_link': 'https://example.com/kendall',
                'image': 'model_kendall.webp'
            },
            {
                'username': 'imaan_hamman',
                'email': 'imaan@example.com',
                'password': 'model123',
                'first_name': 'Imaan',
                'last_name': 'Hamman',
                'gender': 'F',
                'age': 26,
                'height': 178,  # 5'10"
                'measurements': '33-24-35',
                'category': 'Editorial',
                'portfolio_link': 'https://example.com/imaan',
                'image': 'model_imaan.jpg'
            }
        ]
        
        for model_data in models_data:
            if not User.objects.filter(username=model_data['username']).exists():
                # Create user
                user = User.objects.create_user(
                    username=model_data['username'],
                    email=model_data['email'],
                    password=model_data['password'],
                    first_name=model_data['first_name'],
                    last_name=model_data['last_name']
                )
                
                # Create user profile with image
                profile = UserProfile.objects.create(
                    user=user,
                    height=model_data['height'],
                    measurements=model_data['measurements']
                )
                
                # Add profile image
                image_path = self.get_static_image_path(model_data['image'])
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        profile.profile_image.save(model_data['image'], File(f), save=True)
                
                # Create model
                category = ModelCategory.objects.get(name=model_data['category'])
                model = Model.objects.create(
                    user_profile=profile,
                    category=category,
                    gender=model_data['gender'],
                    age=model_data['age'],
                    portfolio_link=model_data['portfolio_link']
                )
        
        self.stdout.write(self.style.SUCCESS('Models created successfully'))

    def seed_magazines(self):
        magazines_data = [
            {
                'title': 'POP MAGAZINE',
                'category': 'Fashion',
                'description': 'Featuring Kendall Jenner on the cover with exclusive fashion editorials.',
                'price': 25.00,
                'publication_date': '2023-06-01',
                'image': 'mag_ken.jpg'
            },
            {
                'title': 'V Magazine',
                'category': 'Fashion',
                'description': 'Featuring Marina Ruy Barbosa with luxury trends.',
                'price': 22.00,
                'publication_date': '2024-05-01',
                'image': 'mag_brazilianmodel.jpg'
            },
            {
                'title': 'VOGUE KOREA',
                'category': 'Lifestyle',
                'description': 'Featuring Lisa Manoban with lifestyle and fashion trends.',
                'price': 20.00,
                'publication_date': '2024-10-01',
                'image': 'mag_lisa.jpeg'
            },
            {
                'title': 'HARPER\'S BAZAAR',
                'category': 'Fashion',
                'description': 'Featuring Jennie Kim with high fashion editorials and trends.',
                'price': 23.00,
                'publication_date': '2023-10-01',
                'image': 'mag_jnk.jpeg'
            }
        ]
        
        for magazine_data in magazines_data:
            category = MagazineCategory.objects.get(name=magazine_data['category'])
            magazine, created = Magazine.objects.get_or_create(
                title=magazine_data['title'],
                defaults={
                    'category': category,
                    'description': magazine_data['description'],
                    'price': magazine_data['price'],
                    'publication_date': magazine_data['publication_date']
                }
            )
            
            # Add cover image
            if created:
                image_path = self.get_static_image_path(magazine_data['image'])
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        magazine.cover_image.save(magazine_data['image'], File(f), save=True)
        
        self.stdout.write(self.style.SUCCESS('Magazines created successfully'))

    def seed_photoshoots(self):
        photoshoots_data = [
            {
                'title': 'Summer Collection 2024',
                'description': 'Exclusive summer fashion collection photoshoot',
                'date': timezone.now() + timedelta(days=30),
                'location': 'Miami Beach, FL',
                'photographer': 'Peter Lindbergh'
            },
            {
                'title': 'Winter Campaign 2024',
                'description': 'Luxury winter fashion campaign',
                'date': timezone.now() + timedelta(days=60),
                'location': 'Aspen, CO',
                'photographer': 'Annie Leibovitz'
            }
        ]
        
        for photoshoot_data in photoshoots_data:
            Photoshoot.objects.get_or_create(
                title=photoshoot_data['title'],
                defaults=photoshoot_data
            )
        
        self.stdout.write(self.style.SUCCESS('Photoshoots created successfully'))

    def seed_runways(self):
        runways_data = [
            {
                'title': 'Paris Fashion Week 2024',
                'description': 'Spring/Summer collection showcase',
                'date': timezone.now() + timedelta(days=45),
                'location': 'Paris, France',
                'designer': 'Chanel'
            },
            {
                'title': 'New York Fashion Week 2024',
                'description': 'Fall/Winter collection showcase',
                'date': timezone.now() + timedelta(days=90),
                'location': 'New York, NY',
                'designer': 'Tom Ford'
            }
        ]
        
        for runway_data in runways_data:
            Runway.objects.get_or_create(
                title=runway_data['title'],
                defaults=runway_data
            )
        
        self.stdout.write(self.style.SUCCESS('Runways created successfully'))

    def seed_campaigns(self):
        campaigns_data = [
            {
                'title': 'Luxury Watch Campaign 2024',
                'description': 'Exclusive campaign for luxury watch brand',
                'start_date': timezone.now(),
                'end_date': timezone.now() + timedelta(days=60),
                'client': 'Rolex'
            },
            {
                'title': 'Perfume Launch 2024',
                'description': 'New perfume launch campaign',
                'start_date': timezone.now() + timedelta(days=30),
                'end_date': timezone.now() + timedelta(days=90),
                'client': 'Dior'
            }
        ]
        
        for campaign_data in campaigns_data:
            Campaign.objects.get_or_create(
                title=campaign_data['title'],
                defaults=campaign_data
            )
        
        self.stdout.write(self.style.SUCCESS('Campaigns created successfully'))

    def handle(self, *args, **options):
        self.stdout.write('Starting database seeding...')
        
        # Ensure static files are collected
        if not settings.STATIC_ROOT:
            self.stdout.write(self.style.WARNING('STATIC_ROOT is not set. Please run "python manage.py collectstatic" first.'))
            return
        
        self.create_superuser()
        self.seed_model_categories()
        self.seed_magazine_categories()
        self.seed_models()
        self.seed_magazines()
        self.seed_photoshoots()
        self.seed_runways()
        self.seed_campaigns()
        
        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!')) 