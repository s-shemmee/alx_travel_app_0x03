from django.contrib import admin
from .models import Listing, Booking, Review


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['name', 'host', 'location', 'pricepernight', 'created_at']
    list_filter = ['location', 'created_at']
    search_fields = ['name', 'location', 'description']
    readonly_fields = ['listing_id', 'created_at', 'updated_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'property', 'user', 'start_date', 'end_date', 'total_price']
    list_filter = ['start_date', 'end_date', 'created_at']
    search_fields = ['property__name', 'user__username']
    readonly_fields = ['booking_id', 'created_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['review_id', 'property', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['property__name', 'user__username', 'comment']
    readonly_fields = ['review_id', 'created_at']
