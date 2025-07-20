#!/usr/bin/env python
"""
Simple test script to verify the ALX Travel App backend is working
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent / 'alx_travel_app'
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')

try:
    django.setup()
    from alx_travel_app.listings.models import Listing, Booking, Review
    from django.contrib.auth.models import User
    
    print("🧪 ALX Travel App Backend Test Results")
    print("=" * 50)
    
    # Test 1: Check database connection
    try:
        user_count = User.objects.count()
        print(f"✅ Database connection: SUCCESS")
        print(f"   Users in database: {user_count}")
    except Exception as e:
        print(f"❌ Database connection: FAILED - {e}")
        sys.exit(1)
    
    # Test 2: Check models
    try:
        listing_count = Listing.objects.count()
        booking_count = Booking.objects.count()
        review_count = Review.objects.count()
        
        print(f"✅ Models working: SUCCESS")
        print(f"   Listings: {listing_count}")
        print(f"   Bookings: {booking_count}")
        print(f"   Reviews: {review_count}")
    except Exception as e:
        print(f"❌ Models: FAILED - {e}")
    
    # Test 3: Check relationships
    try:
        if listing_count > 0:
            first_listing = Listing.objects.first()
            host_name = first_listing.host.username
            reviews_for_listing = first_listing.reviews.count()
            bookings_for_listing = first_listing.bookings.count()
            
            print(f"✅ Relationships working: SUCCESS")
            print(f"   Sample listing: '{first_listing.name}'")
            print(f"   Host: {host_name}")
            print(f"   Reviews for this listing: {reviews_for_listing}")
            print(f"   Bookings for this listing: {bookings_for_listing}")
        else:
            print("⚠️  No listings found - run 'python manage.py seed' first")
    except Exception as e:
        print(f"❌ Relationships: FAILED - {e}")
    
    # Test 4: Check serializers
    try:
        from alx_travel_app.listings.serializers import ListingSerializer, BookingSerializer, ReviewSerializer
        print(f"✅ Serializers imported: SUCCESS")
    except Exception as e:
        print(f"❌ Serializers: FAILED - {e}")
    
    print("=" * 50)
    print("🎉 Backend test completed!")
    print("\n📝 Next steps to test manually:")
    print("1. Open browser: http://127.0.0.1:8000/")
    print("2. Check API docs: http://127.0.0.1:8000/swagger/")
    print("3. Check admin: http://127.0.0.1:8000/admin/")
    
except ImportError as e:
    print(f"❌ Django setup failed: {e}")
    print("Make sure you're running this from the project root directory")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
