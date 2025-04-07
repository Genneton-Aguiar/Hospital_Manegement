from django.test import TestCase
from api.models import Payments, Appointment, Patients, Doctors, Users
from api.repository.payment_repository import PaymentRepository

class PaymentRepositoryTestCase(TestCase):
    def setUp(self):
        
        self.patient_user = Users.objects.create(username="patient_user", is_active=True)
        self.doctor_user = Users.objects.create(username="doctor_user", is_active=True)
        self.patient = Patients.objects.create(user=self.patient_user)
        self.doctor = Doctors.objects.create(user=self.doctor_user, especiality="Cardiology")
        self.appointment = Appointment.objects.create(
            type="geral",
            patient=self.patient,
            doctor=self.doctor,
            date="2025-04-10",
            hour="10:00",
            status_type="agendado"
        )
        self.payment = Payments.objects.create(
            appointment=self.appointment,
            value=100.0,
            payment_type="dinheiro",
            doctor_value=70.0,
            clinic_value=30.0
        )
        self.repository = PaymentRepository()

    def test_retorna_todos_payments(self):

        payments = self.repository.list_all_payments()
        self.assertEqual(len(payments), 1)
        self.assertIn(self.payment, payments)

    def test_retorna_payment_por_id(self):

        payment = self.repository.get_payment_by_id(self.payment.id)
        self.assertEqual(payment, self.payment)

    def test_criação_payment(self):

        new_payment = self.repository.create_payment(
            appointment=self.appointment,
            value=200.0,
            payment_type="dinheiro",
            doctor_value=140.0,
            clinic_value=60.0
        )
        self.assertEqual(new_payment.value, 200.0)
        self.assertEqual(new_payment.payment_type, "dinheiro")
        