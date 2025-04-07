from django.test import TestCase
from api.models import Appointment, Patients, Doctors, Users
from api.repository.appointment_repository import AppointmentRepository

class AppointmentRepositoryTestCase(TestCase):
    def setUp(self):
        # Dados de teste
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
        self.repository = AppointmentRepository()

    def test_todos_appointments(self):
        
        appointments = self.repository.list_all_appointments()
        self.assertEqual(len(appointments), 1)
        self.assertIn(self.appointment, appointments)

    def test_appointment_por_id(self):

        appointment = self.repository.get_appointment_by_id(self.appointment.id)
        self.assertEqual(appointment, self.appointment)

    def test_create_appointment(self):

        new_appointment = self.repository.create_appointment(
            type="geral",
            patient=self.patient,
            doctor=self.doctor,
            date="2025-04-15",
            hour="14:00",
            status_type="agendado"
        )
        self.assertEqual(new_appointment.type, "geral")
        self.assertEqual(new_appointment.date, "2025-04-15")
        self.assertEqual(status_type = "agendado")
    