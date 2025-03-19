from django.urls import path
from . import views

urlpatterns = [
    path('pay/<int:appointment_id>/', views.payment_form, name='payment_form'),
    path('api/payments/process/', views.process_payment, name='process_payment'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
]