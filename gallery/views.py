from django.shortcuts import render
from .models import Photo, PhotoCategory

def landing_page_gallery(request):
    # Get featured photos (or all photos if no featured)
    featured_photos = Photo.objects.filter(is_featured=True).order_by('display_order')[:8]
    
    if not featured_photos.exists():
        featured_photos = Photo.objects.all().order_by('display_order')[:8]
    
    # Get all categories for filtering
    categories = PhotoCategory.objects.filter(is_active=True)
    
    context = {
        'featured_photos': featured_photos,
        'categories': categories,
    }
    return context