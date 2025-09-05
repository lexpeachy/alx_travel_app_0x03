from django.core.management.base import BaseCommand
from listings.models import Listing
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with sample listings"

    def handle(self, *args, **kwargs):
        # Create demo owner
        owner, _ = User.objects.get_or_create(username="demo_owner", defaults={
            "email": "demo@example.com"
        })

        listings_data = [
            {
                "title": "Modern Apartment in Downtown",
                "description": "A stylish apartment close to shopping centers.",
                "address": "123 Main St",
                "city": "New York",
                "country": "USA",
                "price_per_night": 150.00,
                "property_type": "AP",
                "num_bedrooms": 2,
                "num_bathrooms": 1,
                "max_guests": 4,
                "amenities": "WiFi, Air Conditioning, TV",
            },
            {
                "title": "Cozy Mountain Cottage",
                "description": "Perfect for a weekend getaway.",
                "address": "45 Mountain Road",
                "city": "Aspen",
                "country": "USA",
                "price_per_night": 200.00,
                "property_type": "CO",
                "num_bedrooms": 3,
                "num_bathrooms": 2,
                "max_guests": 6,
                "amenities": "Fireplace, Kitchen, Parking",
            },
            {
                "title": "Luxury Villa by the Beach",
                "description": "Enjoy stunning views and private pool.",
                "address": "789 Ocean Drive",
                "city": "Miami",
                "country": "USA",
                "price_per_night": 500.00,
                "property_type": "VI",
                "num_bedrooms": 5,
                "num_bathrooms": 4,
                "max_guests": 10,
                "amenities": "Pool, BBQ, Ocean View",
            },
        ]

        for data in listings_data:
            listing, created = Listing.objects.get_or_create(
                title=data["title"],
                defaults={**data, "owner": owner}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created listing: {listing.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Listing already exists: {listing.title}"))
