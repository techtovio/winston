from django.urls import path
from . import views

urlpatterns = [
    path('ebooks/', views.ebook_list, name='ebook_list'),
    path('ebooks/featured/', views.ebook_list, {'featured': True}, name='featured_ebooks'),
    path('ebooks/category/<int:category_id>/', views.ebook_list, name='ebooks_by_category'),
    path('ebooks/<slug:slug>/', views.ebook_detail, name='ebook_detail'),
    path('ebooks/<slug:slug>/purchase/', views.purchase_options, name='purchase_options'),
    # Add download URL when implementing actual file downloads
]