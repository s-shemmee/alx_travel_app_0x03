from rest_framework import viewsets, permissions
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer

class ListingViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD operations on Listing model"""
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.AllowAny]

class BookingViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD operations on Booking model"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        booking = serializer.save()
        # Extract required info for email
        email = getattr(booking, 'email', None) or 'user@example.com'
        listing_title = getattr(booking, 'listing_title', None) or 'Your Listing'
        check_in = getattr(booking, 'check_in', None) or ''
        check_out = getattr(booking, 'check_out', None) or ''
        # Import and trigger Celery task
        from .tasks import send_booking_confirmation_email
        send_booking_confirmation_email.delay(email, listing_title, check_in, check_out)
