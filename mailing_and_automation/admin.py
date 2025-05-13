# admin.py
from django.contrib import admin
from .models import EmailTemplate, EmailRecipientGroup, DripCampaign, SentEmail
from datetime import timezone, timedelta


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'template_type', 'created_at')
    list_filter = ('template_type',)
    search_fields = ('name', 'subject')
    prepopulated_fields = {'name': ('subject',)}

@admin.register(EmailRecipientGroup)
class EmailRecipientGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_count', 'includes_ebook_downloaders', 'created_at')
    filter_horizontal = ('users',)
    
    def user_count(self, obj):
        return obj.users.count()
    user_count.short_description = 'Users'
    
    def includes_ebook_downloaders(self, obj):
        return obj.ebook_downloaders
    includes_ebook_downloaders.boolean = True
    includes_ebook_downloaders.short_description = 'Ebook Downloaders'

@admin.register(DripCampaign)
class DripCampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'template', 'recipient_group', 'frequency', 'is_active', 'next_send_time')
    list_filter = ('frequency', 'is_active')
    search_fields = ('name', 'template__name', 'recipient_group__name')
    date_hierarchy = 'start_date'
    
    fieldsets = (
        (None, {
            'fields': ('name', 'template', 'recipient_group', 'is_active')
        }),
        ('Schedule', {
            'fields': ('frequency', 'start_date', 'end_date')
        }),
        ('Message', {
            'fields': ('custom_message',),
            'description': 'Add a personal message that will be appended to the template'
        }),
    )
    
    def next_send_time(self, obj):
        if obj.last_sent:
            if obj.frequency == 'daily':
                return obj.last_sent + timedelta(days=1)
            elif obj.frequency == 'weekly':
                return obj.last_sent + timedelta(weeks=1)
            elif obj.frequency == 'monthly':
                # Simple implementation - for exact month calculations you might need a better approach
                return obj.last_sent + timedelta(days=30)
        return obj.start_date
    next_send_time.short_description = 'Next Send Time'

@admin.register(SentEmail)
class SentEmailAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'subject', 'campaign', 'sent_at', 'opened')
    list_filter = ('campaign', 'opened', 'sent_at')
    search_fields = ('recipient', 'subject')
    readonly_fields = ('sent_at', 'opened_at')
    
    def has_add_permission(self, request):
        return False