from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('individual', 'Individual'),
        ('organization', 'Organization'),
        ('government', 'Government'),
    )
    
    # Remove username field and use email as unique identifier
    # username = None
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='individual')
    
    # For organizations/government
    organization_name = models.CharField(max_length=255, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']
    
    def __str__(self):
        #if self.user_type == 'individual':
        #    return f"{self.first_name} {self.last_name}"
        #return self.organization_name or self.email
        return self.email

class About(models.Model):
    about = models.TextField()

    def __str__(self):
        return f'{self.about[0:11]} ...'
