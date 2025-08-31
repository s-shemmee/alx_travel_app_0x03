from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_booking_confirmation(email, booking_id, listing_name):
    subject = "Booking Confirmation"
    message = (
        f"Dear customer,\n\n"
        f"Your booking (ID: {booking_id}) for {listing_name} has been confirmed!\n\n"
        f"Thank you for using ALX Travel App."
    )
    from_email = None  # uses DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
    return f"Booking confirmation sent to {email}"