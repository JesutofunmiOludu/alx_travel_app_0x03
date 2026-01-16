from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

@shared_task
def send_payment_confirmation_email(to_email, booking_reference, amount):
    subject = f"Payment received for booking {booking_reference}"
    message = f"Thank you. We received your payment of {amount} for booking {booking_reference}."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])
    return True