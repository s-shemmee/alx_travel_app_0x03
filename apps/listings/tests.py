
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Listing, Booking

class ListingAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.listing = Listing.objects.create(
            host=self.user,
            name='Test Listing',
            description='A test listing',
            location='Test City',
            pricepernight=100.00
        )

    def test_listings_list(self):
        url = reverse('listing-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_listing(self):
        url = reverse('listing-list')
        data = {
            'host_id': self.user.id,
            'name': 'New Listing',
            'description': 'A new listing',
            'location': 'New City',
            'pricepernight': 150.00
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

class BookingAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser2', password='testpass2')
        self.listing = Listing.objects.create(
            host=self.user,
            name='Test Listing 2',
            description='A test listing 2',
            location='Test City 2',
            pricepernight=200.00
        )

    def test_bookings_list(self):
        url = reverse('booking-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_booking(self):
        url = reverse('booking-list')
        data = {
            'property_id': str(self.listing.listing_id),
            'user_id': self.user.id,
            'start_date': '2025-08-10',
            'end_date': '2025-08-12',
            'total_price': 400.00
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
