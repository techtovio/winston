# models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.conf import settings

User = get_user_model()

class EmailTemplate(models.Model):
    TEMPLATE_TYPES = [
        ('welcome', 'Welcome Email'),
        ('followup', 'Follow-up Email'),
        ('promotional', 'Promotional Email'),
        ('custom', 'Custom Email'),
    ]
    
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES)
    content = models.TextField(help_text="You can use HTML tags for formatting")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class EmailRecipientGroup(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, blank=True)
    ebook_downloaders = models.BooleanField(
        default=False,
        help_text="Include users who downloaded ebooks but didn't register"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_recipients(self):
        recipients = list(self.users.values_list('email', flat=True))
        if self.ebook_downloaders:
            from books.models import EbookPurchase  # Import your actual model
            recipients += list(EbookPurchase.objects.values_list('email', flat=True).distinct())
        return recipients

class DripCampaign(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('once', 'Send Once'),
    ]

    name = models.CharField(max_length=100)
    template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE)
    recipient_group = models.ForeignKey(EmailRecipientGroup, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    custom_message = models.TextField(blank=True, help_text="Add a personal touch to the template")
    created_at = models.DateTimeField(auto_now_add=True)
    last_sent = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class SentEmail(models.Model):
    campaign = models.ForeignKey(DripCampaign, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.EmailField()
    subject = models.CharField(max_length=200)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    opened = models.BooleanField(default=False)
    opened_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.recipient} - {self.subject}"