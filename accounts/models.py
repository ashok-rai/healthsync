from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='PATIENT')
    email = models.EmailField(unique=True)

# class Patient(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
#     # Add patient-specific fields (e.g., date_of_birth)

# class Doctor(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
#     # Add doctor-specific fields (e.g., specialization)