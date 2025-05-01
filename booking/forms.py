from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Booking, SessionType, Location, UnavailableSlot
import datetime

class BookingForm(forms.ModelForm):
    session_type = forms.ModelChoiceField(
        queryset=SessionType.objects.filter(is_active=True),
        widget=forms.RadioSelect(attrs={'class': 'session-type-card'}),
        empty_label=None
    )
    
    location = forms.ModelChoiceField(
        queryset=Location.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Preferred Location"
    )
    
    date = forms.DateField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'bookingDate',
            'placeholder': 'Select date'
        })
    )
    
    time = forms.TimeField(
        widget=forms.HiddenInput(attrs={'id': 'bookingTime'})
    )
    
    terms_accepted = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = Booking
        fields = ['session_type', 'location', 'date', 'time', 'name', 'email', 'phone', 'notes', 'terms_accepted']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise ValidationError("You can't book a session in the past.")
        if date.weekday() >= 5:  # Saturday=5, Sunday=6
            raise ValidationError("We don't book sessions on weekends.")
        return date
    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        location = cleaned_data.get('location')
        
        if date and time and location:
            # Check if slot is already booked
            if Booking.objects.filter(date=date, time=time, location=location).exists():
                raise ValidationError("This time slot is already booked. Please choose another time.")
            
            # Check if slot is marked as unavailable
            from django.db.models import Q
            if UnavailableSlot.objects.filter(
                date=date,
                start_time__lte=time,
                end_time__gt=time
            ).exists():
                raise ValidationError("This time slot is not available. Please choose another time.")
        
        return cleaned_data