from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Listing(models.Model):
    property_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing_image = models.ImageField(upload_to='listing_images/')
    host_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pricetag = models.CharField(max_length=50)
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=4, decimal_places=2)
    property_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  


    def __str__(self):
        return self.title

class Review(models.Model):
    property_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user_id.username} for {self.property_id.title}"

class Booking(models.Model):
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user_id.username} for {self.property_id.title}"

class Payment(models.Model):
    STATUS_PENDING = "Pending"
    STATUS_COMPLETED = "Completed"
    STATUS_FAILED = "Failed"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_FAILED, "Failed"),
    ]
    booking_reference = models.CharField(max_length=128, help_text="Booking reference from bookings table", db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="ETB")
    chapa_tx_id = models.CharField(max_length=256, blank=True, null=True)
    chapa_tx_ref = models.CharField(max_length=256, blank=True, null=True)  # tx_ref
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.booking_reference} - {self.amount} - {self.status}"