
from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
)

from .models import (
    Users, 
    Patients, 
    Doctors, 
    Appointment, 
    Payments
    )

from .serializer import (
    UsersSerializer, 
    PatientsSerializer, 
    DoctorsSerializer, 
    AppointmentSerializer, 
    PaymentsSerializer,
    AdminListSerializer, 
    DoctorListSerializer
    )

from .usecases.user_usecase import UserUseCase
from .repository.user_repository import UserRepository

from .usecases.doctor_usecase import DoctorUseCase
from .repository.doctor_repository import DoctorRepository

from .usecases.patient_usecase import PatientUseCase
from .repository.patient_repository import PatientRepository

from .usecases.appointment_usecase import AppointmentUseCase
from .repository.appointment_repository import AppointmentRepository

from .usecases.payment_usecase import PaymentUseCase
from .repository.payment_repository import PaymentRepository

from .usecases.admin_list_usecase import AdminListUseCase
from .repository.admin_list_repository import AdminListRepository

from .usecases.doctor_list_usecase import DoctorListUseCase
from .repository.doctor_list_repository import DoctorListRepository


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


class DoctorsViewSet(viewsets.ViewSet):
    queryset = Doctors.objects.all()
    serializer_class = DoctorsSerializer
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.doctor_usecase = DoctorUseCase(DoctorRepository(),UserRepository())

    def list(self, request, *args, **kwargs):

        doctors = self.doctor_usecase.list_doctors()
        serializer = DoctorsSerializer(doctors, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        
        try:
            data = request.data
            doctor = self.doctor_usecase.create_doctor(data, request.user)
            serializer = DoctorsSerializer(doctor)
            return Response(serializer.data, status=HTTP_201_CREATED)
        except (PermissionError, ValueError) as e:
            return Response(str(e), status=HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):

        try:
            data = request.data
            doctor = self.doctor_usecase.update_doctor(pk, data, request.user)
            serializer = DoctorsSerializer(doctor)
            return Response(serializer.data, status=HTTP_200_OK)
        except (PermissionError, ValueError) as e:
            return Response(str(e), status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):

        try:
            self.doctor_usecase.delete_doctor(pk, request.user)
            return Response([], status=HTTP_204_NO_CONTENT)
        except (PermissionError, ValueError) as e:
            return Response(str(e), status=HTTP_400_BAD_REQUEST)


class PatientsViewSet(viewsets.ViewSet):
    queryset = Patients.objects.all()
    serializer_class = PatientsSerializer
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.patient_usecase = PatientUseCase(PatientRepository(), UserRepository())

    def list(self, request, *args, **kwargs):
    
        patients = self.patient_usecase.list_patients()
        
        serializer = PatientsSerializer(patients, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
    
        try:
            data = request.data
            patient = self.patient_usecase.create_patient(data, request.user)
            serializer = PatientsSerializer(patient)
            return Response(serializer.data, status=HTTP_201_CREATED)
        except (PermissionError, ValueError) as e:
            return Response(str(e), status=HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        
        try:
            data = request.data
            patient = self.patient_usecase.update_patient(pk, data, request.user)
            serializer = PatientsSerializer(patient)
            return Response(serializer.data, status=HTTP_200_OK)
        except (PermissionError, ValueError) as e:
            return Response(str(e), status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):

        try:
            self.patient_usecase.delete_patient(pk, request.user)
            return Response([], status=HTTP_204_NO_CONTENT)
        except (PermissionError, ValueError) as e:
            return Response(str(e), status=HTTP_400_BAD_REQUEST)
   
    
class AppointmentsViewSet(viewsets.ViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.appointment_usecase = AppointmentUseCase(
            AppointmentRepository(),
            PatientRepository(),
            DoctorRepository()
        )

    def list(self, request, *args, **kwargs):
        """Lista todas as consultas, com filtro opcional por status."""
        status_type = request.GET.get('status_type')
        
        appointments = self.appointment_usecase.list_appointments(status_type)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """Cria uma nova consulta."""
        try:
            data = request.data
            appointment = self.appointment_usecase.create_appointment(data, request.user)
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data, status=HTTP_201_CREATED)
        except (PermissionError, ValueError) as e:
            return Response(str(e), status=HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """Atualiza os dados de uma consulta."""
        try:
            data = request.data
            appointment = self.appointment_usecase.update_appointment(pk, data, request.user)
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data, status=HTTP_200_OK)
        except (PermissionError, ValueError) as e:
            return Response(str(e), status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Desativa uma consulta."""
        try:
            self.appointment_usecase.deactivate_appointment(pk, request.user)
            return Response([], status=HTTP_204_NO_CONTENT)
        except (PermissionError, ValueError) as e:
            return Response(str(e), status=HTTP_400_BAD_REQUEST)
           
    
class PaymentsViewSet(viewsets.ViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.payment_usecase = PaymentUseCase(PaymentRepository(), AppointmentRepository())

    def list(self, request, *args, **kwargs):
    
        payments = self.payment_usecase.list_payments()
        
        serializer = PaymentsSerializer(payments, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        
        try:
            data = request.data
            payment = self.payment_usecase.create_payment(data, request.user)
            serializer = PaymentsSerializer(payment)
            return Response(serializer.data, status=HTTP_201_CREATED)
        except (PermissionError, ValueError) as e:
            return Response(str(e), status=HTTP_400_BAD_REQUEST)


class AdminListViewSet(viewsets.ViewSet):
    queryset = Payments.objects.all()
    serializer_class = AdminListSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.admin_report_usecase = AdminListUseCase(AdminListRepository())

    def list(self, request, *args, **kwargs):

        try:
            report = self.admin_report_usecase.admin_finance_list(request.user)
            return Response(report, status=HTTP_200_OK)
        except PermissionError as e:
            return Response(str(e), status=HTTP_400_BAD_REQUEST)
        
        
class DoctorsListViwSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = DoctorListSerializer
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.doctor_list_usecase = DoctorListUseCase(DoctorListRepository())

    def list(self, request, *args, **kwargs):
        try:
            report = self.doctor_list_usecase.doctor_finance_list(request.user)
            return Response(report, status=HTTP_200_OK)
        except PermissionError as e:
            return Response(str(e), status=HTTP_400_BAD_REQUEST)

