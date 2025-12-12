from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    ROLE_CHOICES = [
        ("buyer", "Buyer"),
        ("supplier", "Supplier"),
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # hashed using set_password()

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    company_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def is_buyer(self):
        return self.role == "buyer"

    def is_supplier(self):
        return self.role == "supplier"

    def __str__(self):
        return f"{self.username} ({self.role})"



class Listing(models.Model):
    CATEGORY_CHOICES = [
        ("raw_material", "Raw Material"),
        ("service", "Service"),
        ("other", "Other"),
    ]

    PRICING_MODE_CHOICES = [
        ("fixed", "Fixed Price"),
        ("rfq_only", "RFQ Only"),
    ]

    supplier = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=255)
    description = models.TextField()
    quantity_available = models.FloatField()
    unit = models.CharField(max_length=50)  # kg, ton, litre
    location_country = models.CharField(max_length=100)

    pricing_mode = models.CharField(max_length=20, choices=PRICING_MODE_CHOICES)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} — {self.supplier.username}"



class PurchaseRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("unpaid", "Unpaid"),
        ("paid", "Paid"),
    ]

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="requests")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer_requests")
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, related_name="supplier_requests")

    requested_quantity = models.FloatField()
    message = models.TextField(blank=True)

    total_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="unpaid")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total(self):
        if self.listing.pricing_mode == "fixed" and self.listing.unit_price:
            qty = Decimal(str(self.requested_quantity))
            price = Decimal(self.listing.unit_price)
            return (qty * price).quantize(Decimal("0.01"))
        return None

    def save(self, *args, **kwargs):
        self.total_amount = self.calculate_total()
        super().save(*args, **kwargs)

    def accept(self):
        if self.listing.quantity_available >= self.requested_quantity:
            self.listing.quantity_available -= self.requested_quantity
            self.listing.save()
        self.status = "accepted"
        self.save()


    def reject(self):
        self.status = "rejected"
        self.save()

    def mark_paid(self):
        self.payment_status = "paid"
        self.save()

    def __str__(self):
        return f"Request #{self.id} — {self.listing.name}"
