from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

from api.models import *
from api.serializer import *

from django.db.models import Q

class TestViews(TestCase):  
    
    def setUp(self):
        
        self.client = APIClient()
        
        self.user_doctor = Users.objects.create(
            username='test_user_doctor', 
            password='test_password',
            is_doctor=True
        )
        
        self.user_patient = Users.objects.create(
            username='test_user_patient', 
            password='test_password',
            is_patient=True
        )
        
        self.admin = Users.objects.create(
                username='test_admin', 
                password='test_password',
                is_admin=True
                )
        
        self.receptionist = Users.objects.create(
            username='test_recepcionist',
            password='test_password',
            is_receptionist=True
        )
        
        self.doctor = Doctors.objects.create(
            user=self.user_doctor,
            especiality='test_especiality'
        )
        
        self.patient = Patients.objects.create(
            
            user=self.user_patient,
            adress='test_adress',
            
        )
        
        self.appointment = Appointment.objects.create(
            
            status_type='AGENDADO',
            type='Consulta',
            patient=self.patient,
            doctor=self.doctor,    
            date='2023-10-25',
            hour='10:00:00',
            is_active=True
            
        )
        
    def teste_de_listagem_de_doutor(self):
    
        response = self.client.get('/api/v1/doctor/',follow=True)
        print(response.status_code)
        
        self.assertEqual(response.status_code, 200)

   
    def teste_criação_de_doutor(self):
        
        self.user = Users.objects.create(
            username='test_user1', 
            password='test_password',
            is_doctor=True
        )
        
        data = {
            'username':'test_user3',
            'user':self.user,
            'especiality':'test_especiality',
        }
        
        
        self.client.force_authenticate(self.admin)
        response = self.client.post('/api/v1/doctor/',data, follow=True)
        
        print(response.status_code)
    
        self.assertEqual(response.status_code, 201)


    def teste_erro_criação_de_doutor_por_falta_de_dados(self):
        
        data = { }
        
        self.client.force_authenticate(self.admin)
        
        response = self.client.post('/api/v1/doctor/',data,follow=True)
        print(response.status_code)
        
        self.assertEqual(response.status_code, 400)
        
        self.assertEqual(
            response.content.decode('utf-8').strip('"'), 
            'informe os dados do medico'
            )
 
 
    def teste_erro_criação_de_doutor_por_falta_de_autenticação(self):
        
        data = { }
        
        self.client.force_authenticate(self.receptionist)
        response = self.client.post('/api/v1/doctor/',data,follow=True)
        print(response.status_code)
        
        self.assertEqual(response.status_code, 400)
        
        
    def teste_edição_de_doutor(self):
   
        data = {
            
            'username':'test_user3',
            'especiality':'test_especiality'
        }   
        
        self.client.force_authenticate(self.admin)
        response = self.client.patch(f'/api/v1/doctor/{self.user_doctor.id}/',data,follow=True)
        
        print(response.status_code)
        
        self.assertEqual(response.status_code, 200)
    
    
    def teste_erro_editação_de_doutor_por_falta_de_dados(self):
        
        data = { }
        
        self.client.force_authenticate(self.admin)
        
        response = self.client.patch(f'/api/v1/doctor/{self.user_doctor.id}/',data,follow=True)
        print(response.status_code)
        
        self.assertEqual(response.status_code, 400)
        
         
    def teste_de_exclusão_de_doutor(self):
        
        self.user = Users.objects.create(
            username='test_user1', 
            password='test_password',
            is_doctor=True
        )
        self.doctor_exclue = Doctors.objects.create(
            user=self.user,
            especiality='urologia'
            
        )
        response = self.client.delete(f'/api/v1/doctor/{self.user.id}/')
        print(response.status_code)
        
        self.assertEqual(response.status_code, 204)
        
        
    def teste_de_listagem_de_paciente (self):

    
        response = self.client.get('/api/v1/patient/',follow=True)
        print(response.status_code)
        
        self.assertEqual(response.status_code, 200) 
      
         
    def teste_criação_de_paciente(self):
        
        data = {
            'username':'test_pactient',
            'adress':'test_adress',
            'phone':'test_phone',
        }
        
        self.client.force_authenticate(self.receptionist)
        response = self.client.post('/api/v1/patient/',data, follow=True)
        
        print(response.status_code)
        
        self.assertEqual(response.status_code, 201)   
        
     
    def teste_erro_criação_de_paciente_por_falta_de_dados(self):
        
        data={ }
        
        self.client.force_authenticate(self.receptionist)
        response = self.client.post('/api/v1/patient/',data, follow=True)
        print(response.status_code)
        
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.data)
        
        self.assertEqual(
            response.content.decode('utf-8').strip('"'), 
            'informe os dados do paciente'
            )
    
    def teste_erro_criação_de_paciente_por_falta_de_autenticação(self):
        
        data = { }
        
        self.client.force_authenticate(self.admin)
        response = self.client.post('/api/v1/patient/',data,follow=True)
        print(response.status_code)
        
        self.assertEqual(response.status_code, 400)
        
        
    def teste_edição_de_paciente(self):
        
        data = {
            'username':'test_pactient',
            'adress':'test_adress',
            'phone':'test_phone',
        }
        
        self.client.force_authenticate(self.receptionist)
        response = self.client.patch(f'/api/v1/patient/{self.user_patient.id}/',data,follow=True)
        
        print(response.status_code)
        
        self.assertEqual(response.status_code, 200)
 
        
    def teste_de_exclusao_de_paciente(self):
        
        self.user = Users.objects.create(
            username='test_user',
            password='test_password',
            is_patient=True
        )

        self.patient_exclue = Patients.objects.create(
            user=self.user,
            adress='test_adress',
            
        )
        
        response = self.client.delete(f'/api/v1/patient/{self.user.id}/')
        print(response.status_code)
        
        self.assertEqual(response.status_code, 204)
    
    
    def teste_erro_editação_de_paciente_por_falta_de_dados(self):   
        
        data={ }
        
        response = self.client.patch(f'/api/v1/patient/{self.user_patient.id}/',data,follow=True)
        print(response.status_code)
        
        self.assertEqual(response.status_code, 400)
        
        
    def teste_de_listagem_de_consulta(self):
        
    
        response = self.client.get('/api/v1/appointment/',follow=True)
        print(response.status_code)
        
        self.assertEqual(response.status_code, 200)     
        
  
    def teste_criação_de_consulta(self):
        
        data = {
            'type': 'Consulta',
            'patient_id': self.user_patient.id,
            'doctor_id': self.user_doctor.id,
            'date': '2024-04-04',
            'hour': '12:00',
            'status_type': 'agendado'
        }
        
        self.client.force_authenticate(self.receptionist)
        response = self.client.post('/api/v1/appointment/',data, follow=True)

        print(response.status_code)
        
        self.assertEqual(response.status_code, 201)
 
   
    def teste_erro_criação_de_consulta_por_falta_de_dados(self):
        
        data={ }
        
        self.client.force_authenticate(self.receptionist)
        response = self.client.post('/api/v1/appointment/',data, follow=True)
        print(response.status_code)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content.decode('utf-8').strip('"'), 
            'informe os dados da consulta'
        )
        
        
    def teste_erro_criação_de_consulta_por_falta_de_autenticação(self):
        
        data = { }
        
        self.client.force_authenticate(self.admin)
        response = self.client.post('/api/v1/appointment/',data,follow=True)
        print(response.status_code)
        
        self.assertEqual(response.status_code, 400)
        
        
    def teste_erro_de_criacao_de_consulta_no_mesmo_horario(self):
        
        data = {
            'type': 'Consulta',
            'patient_id': self.patient.user.id,
            'doctor_id': self.doctor.user.id,
            'date': '2023-10-25',
            'hour': '10:00:00',
            'status_type': 'AGENDADO'
        }
        
        self.client.force_authenticate(self.receptionist)
        response = self.client.post('/api/v1/appointment/', data, follow=True)
        print(response.status_code)
        
        self.appointment_same_hour = Appointment.objects.create(
            type='Consulta',
            patient=self.patient,
            doctor=self.doctor,
            date='2023-10-25',
            hour='10:00:00',
            status_type='AGENDADO'
        )
        
        response = self.client.post('/api/v1/appointment/', data, follow=True)
        self.assertEqual(response.status_code, 400)


    def teste_edição_de_consulta(self):

        data = {
            'status_type': 'REALIZADO',
        }
        
        self.client.force_authenticate(self.user_doctor)
        response = self.client.patch(f'/api/v1/appointment/{self.appointment.id}/',data,follow=True)
        
        print(response.status_code)
        
        self.assertEqual(response.status_code, 200)
    
    
    def teste_erro_edição_de_consulta_por_falta_de_dados(self):
        
        data={ }
        
        self.client.force_authenticate(self.user_doctor)
        response = self.client.patch(f'/api/v1/appointment/{self.appointment.id}/',data,follow=True)
        print(response.status_code)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content.decode('utf-8').strip('"'), 
            'informe os dados da consulta para edição'
        )


    def teste_erro_edição_de_consulta_por_falta_de_autenticação(self):
        
        data={ }
        
        self.client.force_authenticate(self.admin)
        response = self.client.patch(f'/api/v1/appointment/{self.appointment.id}/',data,follow=True)
        print(response.status_code)
        
        self.assertEqual(response.status_code, 400)
        
        
    def teste_de_exclusao_de_consulta(self):
        
        self.appointment = Appointment.objects.create(
            status_type='AGENDADO',
            type='Consulta',
            patient=self.patient,
            doctor=self.doctor,    
            date='2023-10-25',
            hour='10:00:00',
            is_active=True
        )
        
        response = self.client.delete(f'/api/v1/appointment/{self.appointment.id}/')
        print(response.status_code)
        print(response.content)
        self.assertEqual(response.status_code, 204)
  
        
    def teste_autenticação(self):

        
        self.client.force_authenticate(self.admin)
        response = self.client.get('/api/v1/users', follow=True)
            
        print(response.status_code)
        self.assertEqual(response.status_code, 200)
        
                      
    def teste_erro_de_autenticação(self):
            
        self.user = Users.objects.create(
            username='test_user', 
            password='test_password',
            is_admin=False
            )
            

        self.client.force_authenticate(self.user)
            
            
        response = self.client.get('/api/v1/users', follow=True)
        print(response.status_code)
        self.assertEqual(response.status_code, 400 )


    def teste_de_listagem_de_usuarios(self):


        self.client.force_authenticate(self.admin)

        response = self.client.get('/api/v1/users/', follow=True)   
        print(response.status_code)
        
        self.assertEqual(response.status_code, 200)
        
        
    def teste_criação_de_usuario(self):
            
        data={
            'username':'test_user_create',
            'password':'test_password',
            'is_admin':True,
            'is_receptionist':False
        }
        
        self.client.force_authenticate(self.admin)
        response = self.client.post('/api/v1/users/',data, follow=True)
        print(response.status_code)
        
        self.assertEqual(response.status_code, 201)
   
        
    def teste_erro_criação_de_usuario_por_falta_de_dados(self):

        data={ }
        response = self.client.post('/api/v1/users/',data, follow=True)
        print(response.status_code)
        self.assertEqual(response.status_code, 400)


    def teste_de_edição_de_usuario(self):   
        
        self.user_edit= Users.objects.create(
            username='test_user',
            password='test_password',
            is_admin=True
        )
    
        self.client.force_authenticate(self.admin)
        
        update_data = {
            'username': 'updated_user',
            'is_receptionist': True
        }
        
        response = self.client.patch(f'/api/v1/users/{self.user_edit.id}/', update_data)
        print(response.status_code)
        
        self.assertEqual(response.status_code, 200)


    def teste_erro_de_edição_de_usuario_por_falta_de_dados(self):

        update_data = { }
        
        self.client.force_authenticate(self.admin)
        response = self.client.patch(f'/api/v1/users/{self.receptionist.id}/', update_data )
        print(response.status_code)
        
        self.assertEqual(response.status_code, 400)
   
    
    def teste_de_exclusao_de_usuario(self):
        
        self.user = Users.objects.create(
            username='test_user',
            password='test_password',
        )
    
        response = self.client.delete(f'/api/v1/users/{self.user.id}/')
        print(response.status_code)
        
        self.assertEqual(response.status_code, 204)
   
        
#tratamento para caso nao colocar o id quando for excluir um usuario???
    def teste_de_erro_de_exclusao_de_usuario_por_falta_de_id(self):
        
        self.user = Users.objects.create(
            username='test_user',
            password='test_password',
        )
  
        response = self.client.delete(f'/api/v1/users/{self.user}/')
        print(response.status_code)
        
        self.assertEqual(response.status_code, 404)
  
   
    def teste_de_filtro_de_usuarios(self):
        
        self.user_admin = Users.objects.create(
            username='admin_user',
            password='test_password',
            is_admin=True
        )
        
        self.user = Users.objects.create(
            username='receptionist_user',
            password='test_password',
            is_receptionist=True
        )
        
        client = APIClient()
        client.force_authenticate(self.user_admin)
        
        response = client.get('/api/v1/users/?is_admin=True&is_receptionist=True&is_active=True')
        
        self.users = Users.objects.filter(
            Q(is_admin = True) | Q(is_receptionist = True), 
            is_active = True
        )
        
        serializer = UsersSerializer(self.users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)


    def teste_de_erro_de_filtro_de_usuarios(self):
        
        self.user_doctor = Users.objects.create(
            username='doctor_user',
            password='test_password',
            is_doctor=True
        )

        self.user_patient = Users.objects.create(
            username='receptionist_user',
            password='test_password',
            is_patient=True
        )
        
        response = self.client.get('/api/v1/users/?is_admin=True&is_receptionist=True&is_active=True')
        print(response.status_code)
        
        self.assertEqual(response.status_code, 400) 


    def teste_de_filtro_de_consulta(self):
        
        self.appointment_agendado = Appointment.objects.create(
            status_type='AGENDADO',
            type='Consulta',
            patient=None,
            doctor=None,
            date='2023-10-25',
            hour='10:00:00',
            is_active=True
        )
        
        self.appointment_cancelado = Appointment.objects.create(
            status_type='CANCELADO',
            type='Consulta',
            patient=None,
            doctor=None,
            date='2023-10-25',
            hour='11:00:00',
            is_active=True
        )

        self.client.force_authenticate(self.receptionist)

        response = self.client.get('/api/v1/appointment/?status_type=AGENDADO')
        self.assertEqual(response.status_code, 200)


    def teste_listagem_de_payments(self):
        
        self.client.force_authenticate(self.admin)
        
        response = self.client.get('/api/v1/payments/')
        print(response.status_code)
        
        self.assertEqual(response.status_code, 200)
        
               
    def teste_de_criacao_de_payments(self):

        data= {
            'appointment':self.appointment.id,
            'payment_type': 'Cartao',
            'value': 300
        }
        
        self.client.force_authenticate(self.admin)
        
        response = self.client.post('/api/v1/payments/',data,follow=True)
        print(response.status_code)
        
        self.assertEqual(response.status_code, 201)
        
        
    def teste_de_erro_de_criacao_de_payments_por_falta_de_dados(self):
        
        data={ }
        
        self.client.force_authenticate(self.admin)
        response = self.client.post('/api/v1/payments/',data, follow=True)
        
        print(response.status_code)
        
        self.assertEqual(response.status_code, 400)
        
        self.assertEqual(
            response.content.decode('utf-8').strip('"'), 
            'informe os dados do pagamento'
            )
        
        
    def teste_de_erro_de_criacao_de_payments_por_falta_de_autenticacao(self):   
        
        data= { }
        
        
        self.client.force_authenticate(self.receptionist)
        response = self.client.post('/api/v1/payments/',data,follow=True)
        print(response.status_code)
        
        self.assertEqual(response.status_code, 400)


    def teste_listagem_de_payments_para_admins(self):
        
        data = {
            'appointment':self.appointment.id,
            'date': self.appointment.date,
            'doctor': self.user_doctor.username,
            'patient': self.user_patient.username,
            'value': 300,
            'payment_type': 'CARD',
        }
        
        self.client.force_authenticate(self.admin)
        
        response = self.client.get('/api/v1/admlist/',data, follow=True)
        
        print(response.status_code)
        
        self.assertEqual(response.status_code, 200)
    
    
    def teste_listagem_de_payments_para_medicos(self):
        
        
        self.client.force_authenticate(self.user_doctor)
        
        response = self.client.get('/api/v1/doclist/', follow=True)
        
        print(response.status_code)
        print(response.content)
        
        self.assertEqual(response.status_code, 200)
        
        
    def teste_erro_de_listagem_de_payments_para_admins_por_nao_credenciamento(self):
        
        self.client.force_authenticate(self.receptionist)
        
        response = self.client.get('/api/v1/admlist/')
        
        print(response.status_code)
        
        self.assertEqual(response.status_code, 400)
    
    
    def teste_erro_de_listagem_de_payments_para_doctors_por_nao_credenciamento(self):
        
        self.client.force_authenticate(self.receptionist)
        
        response = self.client.get('/api/v1/doclist/')
        
        print(response.status_code)
  
        
        self.assertEqual(response.status_code, 400)
        


    def test_listagem_de_payments_para_admins(self):

        payment1 = Payments.objects.create(
        appointment=self.appointment,
        value=100,
        payment_type='CARD',
        doctor_value=70,
        clinic_value=30
        )

        self.client.force_authenticate(self.admin)

        response = self.client.get('/api/v1/admlist/', follow=True)


        self.assertEqual(response.status_code, 200)


        data = response.json()
        self.assertEqual(len(data), 1)  
        self.assertEqual(data[0]['appointment'], self.appointment.id)
        self.assertEqual(data[0]['date'], self.appointment.date)
        self.assertEqual(data[0]['doctor'], self.user_doctor.username)
        self.assertEqual(data[0]['patient'], self.user_patient.username)
        self.assertEqual(data[0]['value'], 100)
        self.assertEqual(data[0]['payment_type'], 'CARD')


        
    def teste_listagem_de_payments_para_doctors(self):
        
        payment1 = Payments.objects.create(
        appointment=self.appointment,
        value=100,
        payment_type='CARD',
        doctor_value=70,
        clinic_value=30
        )

        
        self.client.force_authenticate(self.user_doctor)
        
        response = self.client.get('/api/v1/doclist/')
        
        print(response.status_code)
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data), 1)  
        self.assertEqual(data[0]['date'], self.appointment.date)
        self.assertEqual(data[0]['patient'], self.user_patient.username)
        self.assertEqual(data[0]['value'], 100)
        self.assertEqual(data[0]['doctor_value'], 70)
        
    