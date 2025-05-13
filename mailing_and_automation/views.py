# Then create a view to handle the tracking:
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SentEmail
from datetime import timezone

@csrf_exempt
def track_email_open(request, email_id):
    try:
        email = SentEmail.objects.get(id=email_id)
        if not email.opened:
            email.opened = True
            email.opened_at = timezone.now()
            email.save()
    except SentEmail.DoesNotExist:
        pass
    
    # Return a transparent 1x1 pixel
    pixel = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
    return HttpResponse(pixel, content_type='image/gif')