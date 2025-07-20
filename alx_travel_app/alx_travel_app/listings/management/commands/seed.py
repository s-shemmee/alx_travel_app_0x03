from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from alx_travel_app.listings.models import Listing, Booking, Review
from decimal import Decimal
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Seed the database with sample listing data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create (default: 10)',
        )
        parser.add_argument(
            '--listings',
            type=int,
            default=20,
            help='Number of listings to create (default: 20)',
        )
        parser.add_argument(
            '--bookings',
            type=int,
            default=15,
            help='Number of bookings to create (default: 15)',
        )
        parser.add_argument(
            '--reviews',
            type=int,
            default=25,
            help='Number of reviews to create (default: 25)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # Create users
        users = self.create_users(options['users'])
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(users)} users')
        )

        # Create listings
        listings = self.create_listings(users, options['listings'])
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(listings)} listings')
        )

        # Create bookings
        bookings = self.create_bookings(users, listings, options['bookings'])
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(bookings)} bookings')
        )

        # Create reviews
        reviews = self.create_reviews(users, listings, options['reviews'])
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(reviews)} reviews')
        )

        self.stdout.write(
            self.style.SUCCESS('Database seeding completed successfully!')
        )

    def create_users(self, count):
        """Create sample users"""
        users = []
        first_names = [
            'John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Chris', 'Anna',
            'Robert', 'Lisa', 'James', 'Maria', 'William', 'Jennifer', 'Richard'
        ]
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
            'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzales'
        ]

        for i in range(count):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = f"{first_name.lower()}{last_name.lower()}{i}"
            email = f"{username}@example.com"

            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password='testpass123'
            )
            users.append(user)

        return users

    def create_listings(self, users, count):
        """Create sample listings"""
        listings = []
        
        # Sample listing data
        property_types = ['Apartment', 'House', 'Villa', 'Condo', 'Studio', 'Loft']
        locations = [
            'New York, NY', 'Los Angeles, CA', 'Chicago, IL', 'Houston, TX',
            'Phoenix, AZ', 'Philadelphia, PA', 'San Antonio, TX', 'San Diego, CA',
            'Dallas, TX', 'San Jose, CA', 'Austin, TX', 'Jacksonville, FL',
            'San Francisco, CA', 'Columbus, OH', 'Charlotte, NC'
        ]
        
        descriptions = [
            'Beautiful and spacious {property_type} in the heart of {location}. Perfect for travelers looking for comfort and convenience.',
            'Modern {property_type} with stunning views and premium amenities. Located in {location} with easy access to attractions.',
            'Cozy and well-furnished {property_type} ideal for business trips or leisure stays in {location}.',
            'Luxury {property_type} featuring elegant design and top-notch facilities in {location}.',
            'Charming {property_type} with unique character and modern conveniences in {location}.',
        ]

        for i in range(count):
            property_type = random.choice(property_types)
            location = random.choice(locations)
            description_template = random.choice(descriptions)
            
            name = f"{property_type} in {location.split(',')[0]}"
            description = description_template.format(
                property_type=property_type.lower(),
                location=location
            )
            price = Decimal(str(random.randint(50, 500)))

            listing = Listing.objects.create(
                host=random.choice(users),
                name=name,
                description=description,
                location=location,
                pricepernight=price
            )
            listings.append(listing)

        return listings

    def create_bookings(self, users, listings, count):
        """Create sample bookings"""
        bookings = []
        
        for i in range(count):
            # Random dates within the next 6 months
            start_date = datetime.now().date() + timedelta(
                days=random.randint(1, 180)
            )
            duration = random.randint(1, 14)  # 1-14 days
            end_date = start_date + timedelta(days=duration)
            
            listing = random.choice(listings)
            user = random.choice([u for u in users if u != listing.host])
            
            # Calculate total price
            total_price = listing.pricepernight * duration
            
            # Check for overlapping bookings
            overlapping = Booking.objects.filter(
                property=listing,
                start_date__lt=end_date,
                end_date__gt=start_date
            ).exists()
            
            if not overlapping:
                booking = Booking.objects.create(
                    property=listing,
                    user=user,
                    start_date=start_date,
                    end_date=end_date,
                    total_price=total_price
                )
                bookings.append(booking)

        return bookings

    def create_reviews(self, users, listings, count):
        """Create sample reviews"""
        reviews = []
        
        review_comments = [
            'Amazing place! Highly recommend to anyone visiting the area.',
            'Clean, comfortable, and exactly as described. Great host!',
            'Perfect location with easy access to all attractions.',
            'Beautiful property with all the amenities you need.',
            'Had a wonderful stay. The host was very responsive.',
            'Great value for money. Would definitely book again.',
            'Excellent communication from the host. Very helpful.',
            'Lovely space with modern furnishings and great views.',
            'Convenient location and comfortable accommodation.',
            'Outstanding property! Exceeded all expectations.',
            'Good place to stay, clean and well-maintained.',
            'Nice property, though a bit smaller than expected.',
            'Decent stay, but could use some improvements.',
            'Average property, nothing special but acceptable.',
        ]

        created_combinations = set()
        
        for i in range(count):
            max_attempts = 50
            attempts = 0
            
            while attempts < max_attempts:
                listing = random.choice(listings)
                user = random.choice([u for u in users if u != listing.host])
                combination = (listing.listing_id, user.id)
                
                if combination not in created_combinations:
                    rating = random.randint(1, 5)
                    # Bias towards higher ratings
                    if random.random() < 0.7:
                        rating = random.randint(4, 5)
                    
                    comment = random.choice(review_comments)
                    
                    review = Review.objects.create(
                        property=listing,
                        user=user,
                        rating=rating,
                        comment=comment
                    )
                    reviews.append(review)
                    created_combinations.add(combination)
                    break
                
                attempts += 1

        return reviews
