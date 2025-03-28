
from rest_framework import viewsets
from rest_framework.response import Response
from .utils import *
from django.db.models import Q

from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
)

from .models import *
from .serializer import *

from .usecases.user_usecase import UserUseCase
from .repository.user_repository import UserRepository

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def list(self, request, *args, **kwargs):
         
        try:
            self.UserUseCase = UserUseCase(UserRepository())
            users = self.UserUseCase.list_adm_receptionists(request.user)
            serializer = UsersSerializer(users, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        except PermissionError as e:
            return Response(str(e), status=HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        
        try:
            self.UserUseCase = UserUseCase(UserRepository())
            data = request.data
            user = self.UserUseCase.create_user(data)
            serializer = UsersSerializer(user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        except ValueError as e:
            return Response(str(e), status=HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
      
        try:
            self.UserUseCase = UserUseCase(UserRepository())
            data= request.data    
            user = self.user_usecase.update_user(pk, data)
            serializer = UsersSerializer(user)
            return Response(serializer.data, status=HTTP_200_OK)
        except ValueError as e:
            return Response(str(e), status=HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        try:
            self.user_usecase = UserUseCase(UserRepository())
            pk = kwargs.get('pk')
            self.user_usecase.delete_user(pk)
            return Response([], status=HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response(str(e), status=HTTP_400_BAD_REQUEST)


class DoctorsViewSet(viewsets.ModelViewSet):
    queryset = Doctors.objects.all()
    serializer_class = DoctorsSerializer

    def list(self, request, *args, **kwargs):   


        doctors = Doctors.objects.all()
        serializer = DoctorsSerializer(doctors, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        
        user = Users.objects.filter(pk = request.user.id).first()
        if not request.user.is_authenticated or not user.is_admin:
            return Response(
                'Desculpe, apenas administradores podem CRIAR medicos',
                status = HTTP_400_BAD_REQUEST
            )

        data = request.data
        if not data:
            return Response(
                'informe os dados do medico', 
                status=HTTP_400_BAD_REQUEST
            )

        doctor = create_doctor(data)
        serializer = self.get_serializer(doctor)
        headers = self.get_success_headers(serializer.data)
        
        return Response(
            serializer.data, 
            status = HTTP_201_CREATED, 
            headers=headers
        )


    def partial_update(self, request, pk):
        
        '''user = Users.objects.filter(pk = request.user.id).first()
        if not request.user.is_authenticated or not user.is_admin:
            return Response(
                'Desculpe, apenas administradores podem EDITAR medicos',
                status = HTTP_400_BAD_REQUEST
            )'''
            
        user = Users.objects.get(pk=pk)
        data = request.data
        if not data:                    
                return Response(
                    'informe os dados do usuario', 
                     status=HTTP_400_BAD_REQUEST
                     )
                
        serializer= UsersSerializer(user,data,partial=True)
        if serializer.is_valid():
                serializer.save()
        return Response(serializer.data,status=HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        
        '''user = Users.objects.filter(pk = request.user.id).first()
        if not request.user.is_authenticated or not user.is_admin:
            return Response(
                'Desculpe, apenas administradores podem DELETAR medicos',
                status = HTTP_400_BAD_REQUEST
            )'''
        
        doctor = self.get_object()
        doctor.delete()
                
        return Response([], status = HTTP_204_NO_CONTENT)


class PatientsViewSet(viewsets.ModelViewSet):
    queryset = Patients.objects.all()
    serializer_class = PatientsSerializer

    def list(self, request, *args, **kwargs):
        '''user = Users.objects.filter(pk = request.user.id).first()
        if not request.user.is_authenticated or not user.is_receptionist:
            return Response(
                'Desculpe, apenas recepcionistas podem LISTAR pacientes',
                status = HTTP_400_BAD_REQUEST
            )'''
            
        patients = Patients.objects.all()
        serializer = PatientsSerializer(patients, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    
    def create(self, request, *args, **kwargs):
        
        
        user = Users.objects.filter(pk = request.user.id).first()
        if not request.user.is_authenticated or not user.is_receptionist:
            return Response(
                'Desculpe, apenas recepcionistas podem CRIAR pacientes',
                status = HTTP_400_BAD_REQUEST
            )

        data = request.data
        if not data:
            return Response(
                'informe os dados do paciente', 
                status=HTTP_400_BAD_REQUEST
            )

        patient = create_patients(data)
        serializer = self.get_serializer(patient)
        headers = self.get_success_headers(serializer.data)
        
        return Response(
            serializer.data, 
            status = HTTP_201_CREATED, 
            headers=headers
        )


    def partial_update(self, request, pk, *args, **kwargs):
        
        '''user = Users.objects.filter(pk = request.user.id).first()
        if not request.user.is_authenticated or not user.is_receptionist:
            return Response(
                'Desculpe, apenas recepcionistas podem EDITAR pacientes',
                status = HTTP_400_BAD_REQUEST
            )'''    
            
        user = Users.objects.get(pk=pk)
        data = request.data
        if not data:                    
                return Response(
                    'informe os dados do usuario', 
                     status=HTTP_400_BAD_REQUEST
                     )
                
        serializer= UsersSerializer(user,data,partial=True)
        if serializer.is_valid():
                serializer.save()
        return Response(serializer.data,status=HTTP_200_OK)
              
                
    def destroy(self, request, *args, **kwargs):
        
        '''user = Users.objects.filter(pk = request.user.id).first()
        if not request.user.is_authenticated or not user.is_receptionist:
            return Response(
                'Desculpe, apenas recepcionistas podem DELETAR pacientes',
                status = HTTP_400_BAD_REQUEST
            )'''
        
        patient = self.get_object()
        patient.delete()
        
        return Response([], status = HTTP_204_NO_CONTENT)
    
    
class AppointmentsViewSet(viewsets.ModelViewSet):
    queryset= Appointment.objects.all()
    serializer_class = AppointmentSerializer
    
    def list(self, request, *args, **kwargs):
        
        
        '''user = Users.objects.filter(pk = request.user.id).first()
        if not request.user.is_authenticated or not user.is_receptionist 
        or not user.is_doctor:
            return Response(
                'Desculpe, apenas recepcionistas podem DELETAR pacientes',
                status = HTTP_400_BAD_REQUEST
            )'''
            
        appointment= Appointment.objects.all()
        
        #filtro para agendamenos por status 
        status = request.GET.get('status_type')
        if status:
                appointment = Appointment.objects.filter(status_type = status)
 
        serializer = AppointmentSerializer(appointment, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
        
        
    def create(self, request, *args, **kwargs):
        
        user = Users.objects.filter(pk = request.user.id).first()
        if not request.user.is_authenticated or not user.is_receptionist: 
            return Response(
                'Apenas recepcionistas OU medicos podem CRIAR consultas',
                status = HTTP_400_BAD_REQUEST
            )
            
        data = request.data
        if not data:
            return Response(
                'informe os dados da consulta', 
                status=HTTP_400_BAD_REQUEST
            )
            
        type = data.get('type')
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        date = data.get('date')
        hour = data.get('hour')
        status_type = data.get('status_type')
        
        
        patient = Patients.objects.get(user_id = patient_id)
        doctor = Doctors.objects.get(user_id = doctor_id)
        
        # verificação de mesmo horario 
        conflicting_appointments = Appointment.objects.filter(
                doctor=doctor,
                date=date, 
                hour=hour,
            ).exists()
        
        if conflicting_appointments == True:
                return Response(
                    'Este médico já tem uma consulta agendada neste horário.',
                    status=HTTP_400_BAD_REQUEST
                ) 

        appointment = Appointment.objects.create(
            type=type,
            patient=patient,
            doctor=doctor,
            date=date,
            hour=hour,
            status_type= status_type
        )

        serializer = self.get_serializer(appointment)
        headers = self.get_success_headers(serializer.data)
        
        return Response(
            serializer.data, 
            status=HTTP_201_CREATED, 
            headers=headers
        )


    def partial_update(self, request, pk):
        
        user = Users.objects.filter(pk = request.user.id).first()
        if not request.user.is_authenticated or not user.is_doctor:
            return Response(
                'Desculpe, apenas Doctors podem editar pacientes',
                status = HTTP_400_BAD_REQUEST
            )
            
        appointment = Appointment.objects.get(pk=pk)
        data = request.data
        if not data:
                return Response(
                        'informe os dados da consulta para edição', 
                        status=HTTP_400_BAD_REQUEST
                )
                    
        serializer= AppointmentSerializer(appointment,data,partial=True)
        if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        
        '''user = Users.objects.filter(pk = request.user.id).first()
        if not request.user.is_authenticated or not user.is_doctor:
            return Response(
                'Desculpe, apenas recepcionistas podem deletar consultas',
                status = HTTP_400_BAD_REQUEST
            )'''
        
        appointment = self.get_object()
        appointment.is_active = False
        appointment.save()  
        
        return Response([], status = HTTP_204_NO_CONTENT)   
    
    
class PaymentsViewSet(viewsets.ModelViewSet):
    queryset= Payments.objects.all()
    serializer_class = PaymentsSerializer

    def list(self, request, *args, **kwargs):    
        
        '''user = Users.objects.filter(pk = request.user.id).first()
        if not request.user.is_authenticated or not user.is_admin:
            return Response(
                'Desculpe, apenas administradores podem LISTAR payments',
                status = HTTP_400_BAD_REQUEST
            )'''
            

        payments= Payments.objects.all()
        serializer = PaymentsSerializer(payments, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        
        user = Users.objects.filter(pk = request.user.id).first()
        if not request.user.is_authenticated or not user.is_admin:
            return Response(
                'Desculpe, apenas administradores podem CRIAR payments',
                status = HTTP_400_BAD_REQUEST
            )
        
        data = request.data
        if not data:
            return Response(
                'informe os dados do pagamento', 
                status=HTTP_400_BAD_REQUEST
            )
        
        value = float(data.get('value',0))
        payment_type = data.get('payment_type')
        
        appointment_id = data.get('appointment')
        appointment = Appointment.objects.get(id = appointment_id)

        # repasse dos medicos
        doctor_value = value * 0.7
        clinic_value = value * 0.3
        
        payments = Payments.objects.create(
            appointment = appointment,
            value=value,
            payment_type=payment_type,
            doctor_value=doctor_value,
            clinic_value=clinic_value
        )

        appointment.is_active = False
        appointment.save()
        
        serializer = self.get_serializer(payments)
        headers = self.get_success_headers(serializer.data)
        
        return Response(
            serializer.data, 
            status=HTTP_201_CREATED, 
            headers=headers
        )


class AdminListViwSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = AdminListSerializer
    
    def list(self, request, *args, **kwargs):
        
        user = Users.objects.filter(pk = request.user.id).first()
        if not request.user.is_authenticated or not user.is_admin:
            return Response(
                'Desculpe, apenas administradores podem visualizar n\
                relatórios financeiros',
                status = HTTP_400_BAD_REQUEST
            )
            
            #relatorio dos administradores 
        list= []
        for payment in self.queryset:
            list.append({
                'appointment': payment.appointment.id,
                'date': payment.appointment.date,
                'doctor': payment.appointment.doctor.user.username,
                'patient': payment.appointment.patient.user.username,
                'value': payment.value,
                'payment_type': payment.payment_type
            })
        
        return Response(
            list,
            status=HTTP_200_OK
        )
        
        
class DoctorsListViwSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()   
    serializer_class = DoctorListSerializer
    
    def list(self, request, *args, **kwargs):
        
        user = Users.objects.filter(pk = request.user.id).first()
        if not request.user.is_authenticated or not user.is_doctor:
            return Response(
                'Desculpe, apenas MEDICOS podem visualizar relatórios financeiros',
                status = HTTP_400_BAD_REQUEST
            )
            
            # relatorio dos medicos
        list= []
        for payment in self.queryset:
            list.append({
                'patient': payment.appointment.patient.user.username,
                'date': payment.appointment.date,
                'value': payment.value,
                'doctor_value': payment.doctor_value,
            })
        
        return Response(
            list,
            status=HTTP_200_OK
        )
            
