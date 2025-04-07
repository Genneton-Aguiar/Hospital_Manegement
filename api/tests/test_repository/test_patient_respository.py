from django.test import TestCase
from api.models import Patients, Users
from api.repository.patient_repository import PatientRepository

class PatientRepositoryTestCase(TestCase):
    def setUp(self):
        # Dados de teste
        self.user = Users.objects.create(username="patient_user", is_active=True)
        self.patient = Patients.objects.create(
            user=self.user,
            birthdate="1990-01-01",
            cpf="12345678900",
            telephone="123456789",
            address="123 Street"
        )
        self.repository = PatientRepository()

    def test_todos_pacientes(self):

        patients = self.repository.list_all_patients()
        self.assertEqual(len(patients), 1)
        self.assertIn(self.patient, patients)

    def test_patient_por_id(self):
        patient = self.repository.get_patient_by_id(self.patient.id)
        self.assertEqual(patient, self.patient)

    def test_create_patient(self):
        
        new_user = Users.objects.create(
            username="test_patient", 
            is_active=True
            )
        patient = self.repository.create_patient(
            user=new_user,
            birthdate="2000-01-01",
            cpf="98765432100",
            telephone="987654321",
            address="456 Avenue"
        )
        self.assertEqual(patient.user.username, "test_patient")
        self.assertEqual(patient.cpf, "98765432100")
        
    