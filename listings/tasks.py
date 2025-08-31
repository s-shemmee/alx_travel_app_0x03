from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_booking_email(user_email, listing_title, start_date, end_date, total_price):
    try:
        send_mail(
            subject='Booking Confirmation',
            message=f'Your booking for {listing_title} has been confirmed.\n\n'
                    f'Dates: {start_date} to {end_date}\n'
                    f'Total Price: ${total_price}\n\n'
                    f'Thank you for booking with us!',
            from_email='noreply@travel_app.com',
            recipient_list=[user_email],
            fail_silently=False,
    )

    except Exception as e:
        print(f"Failed to send email to {user_email}: {e}")
        return f"Details: {e}"