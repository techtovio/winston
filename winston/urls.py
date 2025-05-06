from django.contrib import admin
from django.urls import path, include
from .views import home, about, contact, booking
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.flatpages import views as flatpages_views

admin.site.index_title = "IN WYNSTON WE TRUST"
admin.site.site_header = "IN WYNSTON WE TRUST"
admin.site.site_title =  "IN WYNSTON WE TRUST"


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
path('pages/<path:url>/', flatpages_views.flatpage, name='flatpage'),
path('paypal/', include('paypal.standard.ipn.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
