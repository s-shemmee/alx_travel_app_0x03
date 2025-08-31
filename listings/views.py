import os
import json
import requests
from dotenv import load_dotenv
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views import View
from rest_framework import viewsets
from .models import Listing, Booking, Review, User
from .serializers import (
    ListingSerializer, BookingSerializer,
    ReviewSerializer, UserSerializer
)
from listings.tasks import send_booking_email

load_dotenv()

@method_decorator(csrf_exempt, name='dispatch')
class InitiatePaymentViewSet(View):
    def post(self, request, *args, **kwargs):
        try:
            booking_data = json.loads(request.body)
            url = os.getenv('CHAPA_INITIALIZE_PAYMENT_API_URL')
            headers = {
                "Authorization": f"Bearer {os.getenv('CHAPA_SECRET_KEY')}"
            }
            response = requests.post(url, json=booking_data, headers=headers)
            response.raise_for_status()
            return JsonResponse(response.json())
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing listings.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing bookings.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()

        # Trigger email notification
        send_booking_email.delay(
            user_email=booking.user.email,
            listing_title=booking.listing_id.name,
            start_date=booking.start_date,
            end_date=booking.end_date,
            total_price=booking.total_price
        )
        return super().perform_create(serializer)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


    