# models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='admin_profiles/', null=True, blank=True)
    
    def __str__(self):
        return self.user.get_full_name()