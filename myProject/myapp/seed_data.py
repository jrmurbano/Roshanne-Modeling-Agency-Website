import os
from django.core.files.base import File
from django.conf import settings
from .models import Magazine, MagazineCategory

def create_magazines():
    magazines = [
        {
            'title': 'Vogue',
            'name': 'Vogue Magazine',
            'description': 'The world\'s most influential fashion magazine featuring our top models.',
            'price': 15.99,
            'image': 'mag_anok.jpg',
            'category': 'Fashion'
        },
        {
            'title': 'Elle',
            'name': 'Elle Magazine',
            'description': 'International fashion magazine showcasing our latest fashion campaigns.',
            'price': 12.99,
            'image': 'mag_bella.jpg',
            'category': 'Fashion'
        },
        {
            'title': 'Harper\'s Bazaar',
            'name': 'Harper\'s Bazaar',
            'description': 'American fashion magazine featuring exclusive photoshoots.',
            'price': 14.99,
            'image': 'mag_brazilianmodel.jpg',
            'category': 'Fashion'
        },
        {
            'title': 'GQ',
            'name': 'GQ Magazine',
            'description': 'Men\'s fashion and lifestyle magazine with our male models.',
            'price': 13.99,
            'image': 'mag_jen.jpeg',
            'category': 'Fashion'
        },
        {
            'title': 'Cosmopolitan',
            'name': 'Cosmopolitan',
            'description': 'Women\'s fashion and lifestyle magazine featuring our female models.',
            'price': 11.99,
            'image': 'mag_jnk.jpeg',
            'category': 'Fashion'
        },
        {
            'title': 'Vogue Italia',
            'name': 'Vogue Italia',
            'description': 'Italian edition of Vogue featuring high fashion editorials.',
            'price': 16.99,
            'image': 'mag_ken.jpg',
            'category': 'Fashion'
        },
        {
            'title': 'Vogue Paris',
            'name': 'Vogue Paris',
            'description': 'French edition of Vogue with exclusive fashion spreads.',
            'price': 17.99,
            'image': 'mag_lisa.jpeg',
            'category': 'Fashion'
        },
        {
            'title': 'Vogue US',
            'name': 'Vogue US',
            'description': 'American edition of Vogue featuring our top models.',
            'price': 15.99,
            'image': 'mag_z.jpg',
            'category': 'Fashion'
        }
    ]

    for magazine_data in magazines:
        category = MagazineCategory.objects.get(name=magazine_data['category'])
        magazine = Magazine.objects.create(
            title=magazine_data['title'],
            name=magazine_data['name'],
            description=magazine_data['description'],
            price=magazine_data['price'],
            category=category
        )
        
        # Add cover image
        image_path = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'images', magazine_data['image'])
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                # Save with a unique name in the magazine_covers directory
                magazine.cover_image.save(f"magazine_covers/{magazine_data['title'].lower().replace(' ', '_')}.jpg", File(f), save=True) 