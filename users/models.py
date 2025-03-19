from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('Patient', 'Patient'),
        ('Doctor', 'Doctor'),
        ('Admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='Patient')
    social_auth_id = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def requires_2fa(self):
        return self.role in ['Doctor', 'Admin']

    def __str__(self):
        return self.username