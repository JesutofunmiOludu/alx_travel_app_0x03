from django.contrib import admin
from .models import Listing, Review, Booking, Payment

# Register your models here.

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'state', 'price', 'property_type', 'bedrooms', 'bathrooms', 'created_at')
    list_filter = ('property_type', 'city', 'state', 'created_at')
    search_fields = ('title', 'description', 'address', 'city', 'state')
    readonly_fields = ('property_id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('property_id', 'title', 'description', 'listing_image', 'host_id')
        }),
        ('Location', {
            'fields': ('address', 'city', 'state')
        }),
        ('Property Details', {
            'fields': ('property_type', 'bedrooms', 'bathrooms', 'price', 'pricetag')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'property_id', 'user_id', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('comment', 'user_id__username', 'property_id__title')
    readonly_fields = ('review_id', 'created_at')
    ordering = ('-created_at',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'property_id', 'user_id', 'start_date', 'end_date', 'total_price', 'created_at')
    list_filter = ('start_date', 'end_date', 'created_at')
    search_fields = ('user_id__username', 'property_id__title')
    readonly_fields = ('booking_id', 'created_at')
    ordering = ('-created_at',)
    date_hierarchy = 'start_date'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'amount', 'currency', 'status', 'chapa_tx_ref', 'created_at')
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('booking_reference', 'chapa_tx_id', 'chapa_tx_ref')
    readonly_fields = ('chapa_tx_id', 'chapa_tx_ref', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('booking_reference', 'amount', 'currency')
        }),
        ('Chapa Transaction', {
            'fields': ('chapa_tx_id', 'chapa_tx_ref', 'status')
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

