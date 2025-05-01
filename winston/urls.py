from django.contrib import admin
from django.urls import path, include
from .views import home, about, contact, booking
from django.conf import settings
from django.conf.urls.static import static


admin.site.index_title = "IN WILSON WE TRUST"
admin.site.site_header = "IN WILSON WE TRUST"
admin.site.site_title =  "IN WILSON WE TRUST"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about-us/', about, name='about'),
    path('contact-us/', contact, name='contact'),
    path('accounts/', include('accounts.urls')),
    path('podcasts/', include('podcast.urls')),
    path('ebooks/', include('books.urls')),
    path('booking/', include('booking.urls')),
    path('payments/', include('payments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
