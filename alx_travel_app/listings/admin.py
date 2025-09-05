from django.contrib import admin
from .models import Listing, Booking, Review, Payment


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "city", "country", "price_per_night", "property_type", "owner", "is_active", "created_at")
    search_fields = ("title", "city", "country", "owner__username")
    list_filter = ("property_type", "is_active", "city", "country")
    ordering = ("-created_at",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("listing", "user", "start_date", "end_date", "total_price", "status", "created_at")
    search_fields = ("listing__title", "user__username", "status")
    list_filter = ("status", "start_date", "end_date")
    ordering = ("-created_at",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("listing", "user", "rating", "created_at")
    search_fields = ("listing__title", "user__username")
    list_filter = ("rating", "created_at")
    ordering = ("-created_at",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("booking", "amount", "status", "transaction_id", "created_at")
    search_fields = ("booking__listing__title", "transaction_id", "status")
    list_filter = ("status", "created_at")
    ordering = ("-created_at",)
