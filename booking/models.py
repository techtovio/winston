from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class SessionType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} (${self.price})"

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    is_virtual = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_type = models.ForeignKey(SessionType, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    date = models.DateField()
    time = models.TimeField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmation_code = models.CharField(max_length=20, unique=True, blank=True)
    terms_accepted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['date', 'time']
        unique_together = ['date', 'time', 'location']
    
    def __str__(self):
        return f"Booking #{self.id} - {self.name} - {self.date} {self.time}"
    
    def save(self, *args, **kwargs):
        if not self.confirmation_code:
            self.confirmation_code = self.generate_confirmation_code()
        super().save(*args, **kwargs)
    
    def generate_confirmation_code(self):
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    def get_duration_display(self):
        hours = self.session_type.duration // 60
        minutes = self.session_type.duration % 60
        return f"{hours}h {minutes}m" if hours else f"{minutes}m"

class UnavailableSlot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    reason = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date', 'start_time']
    
    def __str__(self):
        return f"Unavailable: {self.date} {self.start_time}-{self.end_time}"