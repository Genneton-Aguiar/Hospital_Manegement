from django.test import TestCase
from api.models import Doctors, Users
from api.repository.doctor_repository import DoctorRepository

class DoctorRepositoryTestCase(TestCase):
    def setUp(self):
        #dados de teste
        self.user = Users.objects.create(username="doctor_user", is_active=True)
        self.doctor = Doctors.objects.create(user=self.user, especiality="Cardiology")
        self.repository = DoctorRepository()

    def test_list_todos_doctors(self):
        doctors = self.repository.list_all_doctors()
        self.assertEqual(len(doctors), 1)
        self.assertIn(self.doctor, doctors)

    def test_doctor_por_id(self):
        
        doctor = self.repository.get_doctor_by_id(self.doctor.id)
        self.assertEqual(doctor, self.doctor)

    def test_criar_doctor(self):
        
        new_user = Users.objects.create(
            username="test_doctor", 
            is_active=True
            )
        doctor = self.repository.create_doctor(
            user=new_user, 
            especiality="Dermatology"
            )
        self.assertEqual(
            doctor.user.username,
            "test_doctor"
        )
        self.assertEqual(doctor.especiality, "Dermatology")
        