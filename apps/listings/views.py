
from rest_framework import viewsets, permissions
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
import requests
import os
from django.core.mail import send_mail
from django.conf import settings

class InitiatePaymentView(APIView):
    def post(self, request):
        booking_reference = request.data.get('booking_reference')
        amount = request.data.get('amount')
        email = request.data.get('email')
        chapa_url = 'https://api.chapa.co/v1/transaction/initialize'
        headers = {
            'Authorization': f'Bearer {os.getenv("CHAPA_SECRET_KEY")}'
        }
        data = {
            'amount': amount,
            'currency': 'ETB',
            'email': email,
            'tx_ref': booking_reference,
            'callback_url': 'https://yourdomain.com/api/payment/verify/'
        }
        response = requests.post(chapa_url, json=data, headers=headers)
        if response.status_code == 200:
            resp_data = response.json()
            payment = Payment.objects.create(
                booking_reference=booking_reference,
                amount=amount,
                transaction_id=resp_data['data']['tx_ref'],
                status='Pending'
            )
            return Response({'checkout_url': resp_data['data']['checkout_url']}, status=status.HTTP_200_OK)
        return Response({'error': 'Payment initiation failed'}, status=status.HTTP_400_BAD_REQUEST)

class VerifyPaymentView(APIView):
    def get(self, request):
        tx_ref = request.query_params.get('tx_ref')
        chapa_url = f'https://api.chapa.co/v1/transaction/verify/{tx_ref}'
        headers = {
            'Authorization': f'Bearer {os.getenv("CHAPA_SECRET_KEY")}'
        }
        response = requests.get(chapa_url, headers=headers)
        if response.status_code == 200:
            resp_data = response.json()
            try:
                payment = Payment.objects.get(transaction_id=tx_ref)
                if resp_data['data']['status'] == 'success':
                    payment.status = 'Completed'
                    payment.save()
                    # Trigger Celery task for email
                    send_confirmation_email.delay(payment.booking_reference)
                    return Response({'status': 'Payment successful'}, status=status.HTTP_200_OK)
                else:
                    payment.status = 'Failed'
                    payment.save()
                    return Response({'status': 'Payment failed'}, status=status.HTTP_200_OK)
            except Payment.DoesNotExist:
                return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Verification failed'}, status=status.HTTP_400_BAD_REQUEST)

# Celery task for sending confirmation email
from celery import shared_task

@shared_task
def send_confirmation_email(booking_reference):
    # Fetch user email from booking (implement as needed)
    send_mail(
        'Payment Confirmation',
        f'Your payment for booking {booking_reference} was successful.',
        settings.DEFAULT_FROM_EMAIL,
        ['user@example.com'],
        fail_silently=False,
    )

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
