from django.db import models
from users.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialization = models.CharField(max_length=100)
    availability = models.JSONField(default=dict)

    def __str__(self):
        return f"Dr. {self.user.username} - {self.specialization}"