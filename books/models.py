from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()

class EbookCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-book')
    color = models.CharField(max_length=7, default='#1a56db')

    def __str__(self):
        return self.name

class Ebook(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=100)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='ebook_covers/')
    preview_file = models.FileField(upload_to='ebook_previews/', blank=True, null=True)
    file = models.FileField(upload_to='ebooks/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pages = models.PositiveIntegerField()
    publish_date = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField(EbookCategory)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class EbookPurchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, default='M-Pesa')
    payment_confirmation = models.CharField(max_length=100, blank=True)
    is_paid = models.BooleanField(default=False)
    download_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    download_expiry = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.ebook.title} - {self.email}"