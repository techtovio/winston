from django.shortcuts import render
from gallery.models import Photo, PhotoCategory

def home(request):
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
    return render(request, 'home/index.html', context=context)

def contact(request):
    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')

def booking(request):
    return render(request, 'home/booking.html')


'''
def contact(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        name = fname + " " + lname
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        Message.objects.create(name=name, email=email, phone=phone, message=message)
        messages.success(request, "Your message has been submitted successfully, our team will get back to you as soon as possible.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        success_story = Success_Story.objects.all()
        events = Event.objects.filter(is_completed=False)
        projects = Project.objects.all()
        events = Event.objects.all()
        content = {
            'success_story':success_story,
            'events':events,
            'projects':projects,
            'events':events,
        }
        return render(request, 'contact.html', content)
'''