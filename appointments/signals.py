from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment
from notifications.models import Notification
from notifications.tasks import send_sms_notification

@receiver(post_save, sender=Appointment)
def send_appointment_confirmation(sender, instance, created, **kwargs):
    if instance.status == 'Confirmed' and not created:
        message = f"Your appointment with {instance.doctor} on {instance.appointment_date} is confirmed."
        notification = Notification.objects.create(
            user=instance.patient.user,
            message=message
        )
        phone_number = instance.patient.user.phone_number
        send_sms_notification.delay(notification.id, phone_number)