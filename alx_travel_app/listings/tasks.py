from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_booking_confirmation_email(user_email, booking_id, listing_title, start_date, end_date, total_price):
    subject = "Booking Confirmation - ALX Travel App"
    message = (
        f"Hello,\n\n"
        f"Your booking (ID: {booking_id}) for '{listing_title}' has been confirmed.\n"
        f"Check-in: {start_date}\n"
        f"Check-out: {end_date}\n"
        f"Total Price: ${total_price}\n\n"
        f"Thank you for booking with ALX Travel!"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
    return f"Booking confirmation email sent to {user_email}"
