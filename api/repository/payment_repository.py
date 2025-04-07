from api.models import Payments
from django.db import transaction

class PaymentRepository:
    def list_all_payments(self):
       
        return Payments.objects.all()


    def create_payment(self, appointment, value, payment_type, doctor_value, clinic_value):

        with transaction.atomic():
            payment = Payments.objects.create(
                appointment=appointment,
                value=value,
                payment_type=payment_type,
                doctor_value=doctor_value,
                clinic_value=clinic_value
            )
            return payment

