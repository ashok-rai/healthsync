from django.urls import path
from . import views

urlpatterns = [
    path('api/notifications/send/', views.send_appointment_reminder, name='send_reminder'),
]