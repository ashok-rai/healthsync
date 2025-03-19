from django.db import models
from users.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    medical_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username