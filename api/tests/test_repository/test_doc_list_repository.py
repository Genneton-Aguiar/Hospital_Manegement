from django.test import TestCase
from api.models import Payments, Appointment, Patients, Doctors, Users
from api.repository.doctor_list_repository import DoctorListRepository

class DoctorListRepositoryTestCase(TestCase):
    def setUp(self):

        self.doctor_user = Users.objects.create(username="doctor_user", is_active=True)
        self.patient_user = Users.objects.create(username="patient_user", is_active=True)
        self.doctor = Doctors.objects.create(user=self.doctor_user, especiality="pediatra")
        self.patient = Patients.objects.create(user=self.patient_user)
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
        self.repository = DoctorListRepository()

    def test_lista_de_pagamentos(self):
       
        payments = self.repository.list_payments_for_doctor(self.doctor)
        self.assertEqual(len(payments), 1)
        self.assertIn(self.payment, payments)
    