from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.utils import timezone
from datetime import datetime, timedelta
from .models import SessionType, Location, Booking, UnavailableSlot
from .forms import BookingForm
import json

def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            
            # If user is authenticated, associate with booking
            if request.user.is_authenticated:
                booking.user = request.user
            
            booking.save()
            
            # Send confirmation email
            send_booking_confirmation(booking)
            
            messages.success(request, f"Booking confirmed! A confirmation has been sent to {booking.email}.")
            return redirect('booking_success', booking_id=booking.id)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial.update({
                'name': request.user.get_full_name(),
                'email': request.user.email,
                'phone': request.user.phone_number
            })
        form = BookingForm(initial=initial)
    
    session_types = SessionType.objects.filter(is_active=True)
    locations = Location.objects.filter(is_active=True)
    
    return render(request, 'home/booking.html', {
        'form': form,
        'session_types': session_types,
        'locations': locations,
    })

def booking_success(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'home/booking_success.html', {'booking': booking})

@require_GET
def get_available_times(request):
    date_str = request.GET.get('date')
    location_id = request.GET.get('location')
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        location = Location.objects.get(id=location_id)
    except (ValueError, Location.DoesNotExist):
        return JsonResponse({'error': 'Invalid date or location'}, status=400)
    
    # Define working hours (9AM-5PM)
    start_time = datetime.combine(date, datetime.strptime('09:00', '%H:%M').time())
    end_time = datetime.combine(date, datetime.strptime('17:00', '%H:%M').time())
    
    # Generate all possible 30-minute slots
    all_slots = []
    current = start_time
    while current < end_time:
        all_slots.append(current.time())
        current += timedelta(minutes=30)
    
    # Get booked slots
    booked_slots = Booking.objects.filter(
        date=date,
        location=location
    ).values_list('time', flat=True)
    
    # Get unavailable slots
    unavailable_slots = UnavailableSlot.objects.filter(date=date).values_list('start_time', 'end_time')
    
    # Filter available slots
    available_slots = []
    for slot in all_slots:
        slot_datetime = datetime.combine(date, slot)
        
        # Check if slot is booked
        if slot in booked_slots:
            continue
        
        # Check if slot is marked as unavailable
        unavailable = False
        for start, end in unavailable_slots:
            if start <= slot < end:
                unavailable = True
                break
        if unavailable:
            continue
        
        available_slots.append(slot.strftime('%H:%M'))
    
    return JsonResponse({'times': available_slots})

def send_booking_confirmation(booking):
    subject = f"Booking Confirmation: {booking.session_type.name}"
    message = f"""
    Thank you for booking a session with In Wilson We Trust!
    
    Booking Details:
    - Type: {booking.session_type.name}
    - Date: {booking.date.strftime('%A, %B %d, %Y')}
    - Time: {booking.time.strftime('%I:%M %p')} EAT
    - Duration: {booking.get_duration_display()}
    - Location: {booking.location.name}
    - Confirmation Code: {booking.confirmation_code}
    
    Notes: {booking.notes or 'None'}
    
    We look forward to seeing you!
    
    Best regards,
    The Wilson Team
    """
    
    # In production, you would actually send the email
    print(f"Email would be sent to {booking.email} with subject: {subject}")
    print(message)
    
    # Uncomment to actually send emails
    # send_mail(
    #     subject,
    #     message,
    #     settings.DEFAULT_FROM_EMAIL,
    #     [booking.email],
    #     fail_silently=False,
    # )
    
    # Also send notification to admin
    admin_message = f"""
    New Booking Received:
    
    {str(booking)}
    
    Contact: {booking.name} ({booking.email}, {booking.phone})
    """
    
    # send_mail(
    #     f"New Booking: {booking.confirmation_code}",
    #     admin_message,
    #     settings.DEFAULT_FROM_EMAIL,
    #     [settings.ADMIN_EMAIL],
    #     fail_silently=False,
    # )