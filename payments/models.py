from django.db import models
#from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from accounts.models import User

class Plan(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    usd_price = models.DecimalField(max_digits=10, decimal_places=2)
    kes_price = models.DecimalField(max_digits=10, decimal_places=2)
    tzs_price = models.DecimalField(max_digits=10, decimal_places=2)
    ugx_price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField(help_text="One feature per line")

    def __str__(self):
        return self.name

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('MPESA', 'M-Pesa'),
        ('AIRTEL', 'Airtel Money'),
        ('CARD', 'Credit/Debit Card'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    phone_number = models.CharField(max_length=20)
    country_code = models.CharField(max_length=5)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # For guest checkout
    guest_email = models.EmailField(blank=True)
    guest_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Payment #{self.id} - {self.get_status_display()}"

    def get_full_phone(self):
        return f"{self.country_code}{self.phone_number}"
    

class EbookFlash(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    amount = models.FloatField(default=0, max_length=10)
    ref_id = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} paid Ksh {self.amount}'