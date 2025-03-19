import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from appointments.models import Appointment
import logging

stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)

def payment_form(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if request.user != appointment.patient.user:
        return JsonResponse({"error": "Unauthorized"}, status=403)
    
    context = {
        'appointment': appointment,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'payments/payment_form.html', context)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_payment(request):
    appointment_id = request.data.get('appointment_id')
    token = request.data.get('stripe_token')
    
    try:
        appointment = Appointment.objects.get(id=appointment_id, patient__user=request.user)
        amount = 5000  # $50.00 in cents
        idempotency_key = f"payment_{appointment_id}_{request.user.id}"

        charge = stripe.Charge.create(
            amount=amount,
            currency='usd',
            source=token,
            description=f"Payment for appointment {appointment_id}",
            idempotency_key=idempotency_key,
        )

        payment, created = Payment.objects.get_or_create(
            appointment=appointment,
            defaults={'amount': amount / 100, 'payment_status': 'Paid', 'transaction_id': charge.id}
        )
        if not created:
            payment.payment_status = 'Paid'
            payment.transaction_id = charge.id
            payment.save()

        appointment.payment_status = 'Paid'
        appointment.save()

        logger.info(f"Payment successful for appointment {appointment_id}: {charge.id}")
        return JsonResponse({"message": "Payment successful", "transaction_id": charge.id})

    except stripe.error.CardError as e:
        logger.error(f"Payment failed for appointment {appointment_id}: {str(e)}")
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({"error": "An error occurred"}, status=500)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return JsonResponse({"error": "Invalid payload"}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({"error": "Invalid signature"}, status=400)

    if event['type'] == 'charge.succeeded':
        charge = event['data']['object']
        transaction_id = charge['id']
        payment = Payment.objects.get(transaction_id=transaction_id)
        payment.payment_status = 'Paid'
        payment.save()
        payment.appointment.payment_status = 'Paid'
        payment.appointment.save()
        logger.info(f"Webhook: Charge succeeded for {transaction_id}")

    return JsonResponse({"status": "success"})