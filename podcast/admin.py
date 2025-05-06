from django.contrib import admin
from .models import Podcast, PodcastCategory

admin.site.register(PodcastCategory)
admin.site.register(Podcast)
