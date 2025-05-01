from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.booking_view, name='booking'),
    path('book/success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('book/available-times/', views.get_available_times, name='available_times'),
]