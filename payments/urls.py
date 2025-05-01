from django.urls import path
from .views import PlanListView, initiate_payment, payment_success, payment_failure

urlpatterns = [
    path('plans/', PlanListView.as_view(), name='plans'),
    path('pay/', initiate_payment, name='initiate_payment'),
    path('payment/success/', payment_success, name='payment_success'),
    path('payment/failure/', payment_failure, name='payment_failure'),
]