from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from appointments.models import Appointment
from .models import Notification
from .tasks import send_sms_notification
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_appointment_reminder(request):
    appointment_id = request.data.get('appointment_id')
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        if request.user.role == 'Admin' or request.user == appointment.patient.user:
            message = f"Reminder: Your appointment with {appointment.doctor} is on {appointment.appointment_date}."
            notification = Notification.objects.create(
                user=appointment.patient.user,
                message=message
            )
            phone_number = appointment.patient.user.phone_number
            send_sms_notification.delay(notification.id, phone_number)
            logger.info(f"Queued SMS for appointment {appointment_id}")
            return JsonResponse({"message": "Notification queued"})
        return JsonResponse({"error": "Unauthorized"}, status=403)
    except Exception as e:
        logger.error(f"Error queuing notification: {str(e)}")
        return JsonResponse({"error": "An error occurred"}, status=500)