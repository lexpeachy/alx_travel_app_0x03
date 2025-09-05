from rest_framework import serializers
from .models import Listing, Booking, Review


class ListingSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id", "title", "description", "address", "city", "country",
            "price_per_night", "property_type", "num_bedrooms",
            "num_bathrooms", "max_guests", "amenities", "owner",
            "created_at", "updated_at", "is_active"
        ]


class BookingSerializer(serializers.ModelSerializer):
    listing = serializers.StringRelatedField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id", "listing", "user", "start_date", "end_date",
            "total_price", "status", "created_at"
        ]


class ReviewSerializer(serializers.ModelSerializer):
    listing = serializers.StringRelatedField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "listing", "user", "rating", "comment", "created_at"]

from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "booking", "transaction_id", "amount", "status", "created_at", "updated_at"]
        read_only_fields = ["transaction_id", "status", "created_at", "updated_at"]
