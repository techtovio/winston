from django.contrib import admin
from .models import Photo, PhotoCategory

@admin.register(PhotoCategory)
class PhotoCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_order', 'is_featured', 'created_at')
    list_editable = ('display_order', 'is_featured')
    list_filter = ('is_featured', 'categories')
    search_fields = ('title', 'description')
    filter_horizontal = ('categories',)
    prepopulated_fields = {'slug': ('title',)}