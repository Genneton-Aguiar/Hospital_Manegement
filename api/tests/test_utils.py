from django.test import TestCase

from api.models import *
from api.serializer import *

from django.db.models import Q


class TestViews(TestCase):  
    
    def teste_de_create_ususario(self):
        
        self.user = Users.objects.create(
            username='test_user',
            password='test_password',
            is_admin=True
        )
        
        self.assertEqual(self.user.username, 'test_user')
        self.assertEqual(self.user.is_admin, True)
        self.assertEqual(self.user.password, 'test_password')
    
    def teste_de_create_doctor (self):
        
        self.user = Users.objects.create(
            username='test_user',
            password='test_password',
            is_doctor=True
        )
        
        self.doctor = Doctors.objects.create(
            user=self.user,
            especiality='test_especiality'
        )
        
        self.assertEqual(self.doctor.user, self.user)
        
        self.assertEqual(self.doctor.especiality, 'test_especiality')
        
    def teste_de_create_paciente (self):
        
         
        self.user = Users.objects.create(
        is_patient=True
    )
    
        self.patients = Patients.objects.create(
        user=self.user,
        birthdate='2024-04-04',
        cpf='000-000',
        telephone='000',
        adress='test_adress',
    )
    
        self.assertEqual(self.patients.user, self.user)
        self.assertEqual(self.patients.birthdate, '2024-04-04')
        self.assertEqual(self.patients.cpf, '000-000')
        self.assertEqual(self.patients.telephone, '000')
        self.assertEqual(self.patients.adress, 'test_adress')
            
