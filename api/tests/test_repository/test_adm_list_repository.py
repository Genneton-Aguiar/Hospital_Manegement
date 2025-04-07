from django.test import TestCase
from api.models import Payments, Appointment, Patients, Doctors, Users
from api.repository.admin_list_repository import AdminListRepository

class AdminListRepositoryTestCase(TestCase):
    def setUp(self):
        """Configura os dados de teste."""
        self.patient_user = Users.objects.create(username="patient_user", is_active=True)
        self.doctor_user = Users.objects.create(username="doctor_user", is_active=True)
        self.patient = Patients.objects.create(user=self.patient_user)
        self.doctor = Doctors.objects.create(user=self.doctor_user, especiality="Cardiology")
        self.appointment = Appointment.objects.create(
            type="Consultation",
            patient=self.patient,
            doctor=self.doctor,
            date="2025-04-10",
            hour="10:00",
            status_type="Scheduled"
        )
        self.payment = Payments.objects.create(
            appointment=self.appointment,
            value=100.0,
            payment_type="Credit Card",
            doctor_value=70.0,
            clinic_value=30.0
        )
        self.repository = AdminListRepository()

    def test_list_all_payments(self):
 
        payments = self.repository.list_all_payments()
        self.assertEqual(len(payments), 1)
        self.assertIn(self.payment, payments)
        