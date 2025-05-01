from django.contrib import admin
from .models import SessionType, Location, Booking, UnavailableSlot

@admin.register(SessionType)
class SessionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'price', 'is_active')
    list_editable = ('is_active',)
    #prepopulated_fields = {'slug': ('name',)}

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_virtual', 'is_active')
    list_editable = ('is_active',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('confirmation_code', 'name', 'session_type', 'date', 'time', 'location', 'status')
    list_filter = ('status', 'session_type', 'location', 'date')
    search_fields = ('name', 'email', 'phone', 'confirmation_code')
    readonly_fields = ('created_at', 'updated_at', 'confirmation_code')

@admin.register(UnavailableSlot)
class UnavailableSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'end_time', 'reason')
    list_filter = ('date',)