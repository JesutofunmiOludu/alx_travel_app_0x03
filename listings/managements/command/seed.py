
from django.core.management.base import BaseCommand
from listings.models import Listing
from django.contrib.auth import get_user_model
import random

User = get_user_model()

SAMPLE_LISTINGS = [
    {
        "title": "Modern Beach House",
        "description": "A beautiful beach house with a stunning ocean view.",
        "price_per_night": 250.00,
        "location": "Lagos, Nigeria"
    },
    {
        "title": "Cozy Mountain Cabin",
        "description": "Warm and peaceful cabin perfect for vacations.",
        "price_per_night": 180.00,
        "location": "Obudu, Nigeria"
    },
    {
        "title": "Luxury Apartment",
        "description": "A fully serviced luxury apartment in the heart of the city.",
        "price_per_night": 300.00,
        "location": "Abuja, Nigeria"
    }
]


class Command(BaseCommand):

    help = "Seed the database with sample listings"

    def handle(self, *args, **kwargs):
        # Create admin user if not exists
        user, created = User.objects.get_or_create(
            email="host@example.com",
            defaults={
                "first_name": "Host",
                "last_name": "User",
                "password": "adminpass123",
            }
        )

        if created:
            user.set_password("adminpass123")
            user.save()

        self.stdout.write(self.style.SUCCESS("Host user ready."))

        # Insert Sample Listings
        for data in SAMPLE_LISTINGS:
            Listing.objects.get_or_create(
                title=data["title"],
                defaults={
                    "description": data["description"],
                    "price_per_night": data["price_per_night"],
                    "location": data["location"],
                    "host": user
                }
            )

        self.stdout.write(self.style.SUCCESS("Sample listings created successfully!"))
