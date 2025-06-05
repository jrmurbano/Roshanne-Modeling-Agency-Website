def create_magazines():
    magazines = [
        {
            'title': 'Vogue',
            'name': 'Vogue Magazine',
            'description': 'The world\'s most influential fashion magazine featuring our top models.',
            'price': 15.99,
            'image': 'magazines/mag_anok.jpg',
            'category': 'Fashion'
        },
        {
            'title': 'Elle',
            'name': 'Elle Magazine',
            'description': 'International fashion magazine showcasing our latest fashion campaigns.',
            'price': 12.99,
            'image': 'magazines/mag_bella.jpg',
            'category': 'Fashion'
        },
        {
            'title': 'Harper\'s Bazaar',
            'name': 'Harper\'s Bazaar',
            'description': 'American fashion magazine featuring exclusive photoshoots.',
            'price': 14.99,
            'image': 'magazines/mag_brazilianmodel.jpg',
            'category': 'Fashion'
        },
        {
            'title': 'GQ',
            'name': 'GQ Magazine',
            'description': 'Men\'s fashion and lifestyle magazine with our male models.',
            'price': 13.99,
            'image': 'magazines/mag_jen.jpeg',
            'category': 'Fashion'
        },
        {
            'title': 'Cosmopolitan',
            'name': 'Cosmopolitan',
            'description': 'Women\'s fashion and lifestyle magazine featuring our female models.',
            'price': 11.99,
            'image': 'magazines/mag_jnk.jpeg',
            'category': 'Fashion'
        },
        {
            'title': 'Vogue Italia',
            'name': 'Vogue Italia',
            'description': 'Italian edition of Vogue featuring high fashion editorials.',
            'price': 16.99,
            'image': 'magazines/mag_ken.jpg',
            'category': 'Fashion'
        },
        {
            'title': 'Vogue Paris',
            'name': 'Vogue Paris',
            'description': 'French edition of Vogue with exclusive fashion spreads.',
            'price': 17.99,
            'image': 'magazines/mag_lisa.jpeg',
            'category': 'Fashion'
        },
        {
            'title': 'Vogue US',
            'name': 'Vogue US',
            'description': 'American edition of Vogue featuring our top models.',
            'price': 15.99,
            'image': 'magazines/mag_z.jpg',
            'category': 'Fashion'
        }
    ]

    for magazine_data in magazines:
        category = MagazineCategory.objects.get(name=magazine_data['category'])
        Magazine.objects.create(
            title=magazine_data['title'],
            name=magazine_data['name'],
            description=magazine_data['description'],
            price=magazine_data['price'],
            image=magazine_data['image'],
            category=category
        ) 