from django.test import TestCase
from api.models import *
from api.serializer import UsersSerializer


class usersTest(TestCase):
    
    def teste_criação_recepcionista(self):
        
        expected_data = {
            "username": "test_user",
            "password": "test_password",
            "email": "test_email",
            "is_admin": False,
            "is_receptionist": True,
            "is_doctor": False,
            "is_patient": False
        }
        
        user = Users.objects.create(**expected_data)
        user_data = UsersSerializer(user, many=False).data
        user_data.pop('id')
        expected_data.pop('password')
        expected_data.pop('email')

        self.assertEqual(user_data, expected_data)

    def teste_str_users(self):
        
        user = User.objects.create_user(username='test_user')
        self.assertEqual(str(user), 'test_user')

    def teste_str_doctors(self):
        user = Users.objects.create_user(username='test_user')
        model = Doctors.objects.create(user=user)
        
        self.assertEqual(str(model), 'test_user')


    def teste_str_patients(self):   
        
        user = Users.objects.create_user(username='test_user')
        model = Patients.objects.create(user=user)
        
        self.assertEqual(str(model), 'test_user')
    

    def teste_str_appointments(self):
        date = '2023-10-25'
        modelo = Appointment.objects.create(date=date)
        self.assertEqual(str(modelo), date)
    
    
       
        