from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class PodcastCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")

    def __str__(self):
        return self.name

class Podcast(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    audio_file = models.FileField(upload_to='podcasts/')
    thumbnail = models.ImageField(upload_to='podcast_thumbnails/')
    duration = models.DurationField(help_text="HH:MM:SS format")
    publish_date = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField(PodcastCategory)
    is_premium = models.BooleanField(default=False)
    allowed_user_types = models.CharField(
        max_length=100,
        default='individual,organization,government',
        help_text="Comma-separated list of allowed user types (individual,organization,government)"
    )

    def __str__(self):
        return self.title

    def user_can_access(self, user):
        if not self.is_premium:
            return True
        
        if not user.is_authenticated:
            return False
        
        # Check if user type is allowed
        allowed_types = [t.strip() for t in self.allowed_user_types.split(',')]
        if user.user_type not in allowed_types:
            return False
            
        # Check if user has active subscription
        return Subscription.objects.filter(
            user=user,
            is_active=True,
            valid_until__gte=timezone.now()
        ).exists()

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField(help_text="Duration in days")
    allowed_user_types = models.CharField(
        max_length=100,
        default='individual,organization,government',
        help_text="Comma-separated list of allowed user types (individual,organization,government)"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (${self.price})"

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    subscribed_on = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            self.valid_until = timezone.now() + timezone.timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)