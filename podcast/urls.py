from django.urls import path
from . import views

urlpatterns = [
    path('podcasts/', views.podcast_list, name='podcast_list'),
    path('podcasts/<int:pk>/', views.podcast_detail, name='podcast_detail'),
    path('subscription-plans/', views.subscription_plans, name='subscription_plans'),
    # Add payment handling URLs as needed
]