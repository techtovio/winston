# templates_handler/admin.py
from django.contrib import admin
from .models import ContentContainer, ContentItem, TeamMember, Testimonial

class ContentItemInline(admin.TabularInline):
    model = ContentItem
    extra = 1
    fields = ('title', 'content', 'image', 'image_alt', 'image_position', 'button_text', 'button_url', 'order', 'is_active')
    ordering = ('order',)

class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1
    fields = ('name', 'position', 'bio', 'image', 'email', 'phone', 'social_media', 'order')
    ordering = ('order',)

class TestimonialInline(admin.TabularInline):
    model = Testimonial
    extra = 1
    fields = ('author', 'position', 'content', 'image', 'rating', 'order')
    ordering = ('order',)

@admin.register(ContentContainer)
class ContentContainerAdmin(admin.ModelAdmin):
    list_display = ('name', 'container_type', 'page_location', 'order', 'is_active')
    list_filter = ('container_type', 'page_location', 'is_active')
    search_fields = ('name',)
    ordering = ('order', 'name')
    inlines = [ContentItemInline, TeamMemberInline, TestimonialInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'container_type', 'page_location', 'order', 'is_active')
        }),
    )

admin.site.register(ContentItem)
admin.site.register(TeamMember)
admin.site.register(Testimonial)
