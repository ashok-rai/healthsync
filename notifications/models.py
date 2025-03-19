from django.db import models
from users.models import User

class Notification(models.Model):
    STATUS_CHOICES = (
        ('Sent', 'Sent'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - {self.status}"