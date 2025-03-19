from celery import shared_task
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings
import logging
from .models import Notification

logger = logging.getLogger(__name__)
client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

@shared_task(bind=True, max_retries=3)
def send_sms_notification(self, notification_id, to_phone_number):
    try:
        notification = Notification.objects.get(id=notification_id)
        message = client.messages.create(
            body=notification.message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_phone_number
        )
        notification.status = 'Sent'
        notification.save()
        logger.info(f"SMS sent to {to_phone_number}: {message.sid}")
    except TwilioRestException as e:
        logger.error(f"Failed to send SMS: {str(e)}")
        notification.status = 'Failed'
        notification.save()
        try:
            self.retry(countdown=60)
        except self.MaxRetriesExceededError:
            logger.error(f"Max retries exceeded for notification {notification_id}")