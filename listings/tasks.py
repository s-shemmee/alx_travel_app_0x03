from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_booking_confirmation_email(email, listing_title, check_in, check_out):
    subject = f'Booking Confirmation: {listing_title}'
    message = f'Your booking from {check_in} to {check_out} has been confirmed.'
    from_email = None
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)