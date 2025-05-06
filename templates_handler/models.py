# templates_handler/models.py
from django.db import models
from django.utils.text import slugify
from django.utils import timezone

class ContentContainer(models.Model):
    CONTAINER_TYPES = (
        ('plain_text', 'Plain Text'),
        ('image_text', 'Image with Text'),
        ('gallery', 'Image Gallery'),
        ('card', 'Card Layout'),
        ('accordion', 'Accordion'),
        ('contact_form', 'Contact Form'),
        ('team', 'Team Members'),
        ('testimonial', 'Testimonials'),
    )
    
    PAGE_LOCATIONS = (
        ('landing', 'Landing Page'),
        ('about', 'About Page'),
        ('contact', 'Contact Page'),
        ('all', 'All Pages'),
    )
    
    name = models.CharField(max_length=100)
    container_type = models.CharField(max_length=50, choices=CONTAINER_TYPES)
    page_location = models.CharField(max_length=50, choices=PAGE_LOCATIONS)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Content Container'
        verbose_name_plural = 'Content Containers'
    
    def __str__(self):
        return f"{self.name} ({self.get_container_type_display()})"

class ContentItem(models.Model):
    container = models.ForeignKey(ContentContainer, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='content_images/', blank=True, null=True)
    image_alt = models.CharField(max_length=200, blank=True, null=True)
    image_position = models.CharField(
        max_length=10,
        choices=(('left', 'Left'), ('right', 'Right'), ('top', 'Top'), ('bottom', 'Bottom')),
        default='left',
        blank=True,
        null=True
    )
    button_text = models.CharField(max_length=50, blank=True, null=True)
    button_url = models.CharField(max_length=200, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Content Item'
        verbose_name_plural = 'Content Items'
    
    def __str__(self):
        return self.title if self.title else f"Item {self.id}"

class TeamMember(models.Model):
    container = models.ForeignKey(ContentContainer, on_delete=models.CASCADE, related_name='team_members')
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='team_images/')
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    social_media = models.JSONField(blank=True, null=True)  # Stores {'twitter': 'url', 'linkedin': 'url', etc.}
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name

class Testimonial(models.Model):
    container = models.ForeignKey(ContentContainer, on_delete=models.CASCADE, related_name='testimonials')
    author = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    image = models.ImageField(upload_to='testimonial_images/', blank=True, null=True)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Testimonial by {self.author}"
