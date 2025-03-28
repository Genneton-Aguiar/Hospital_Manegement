from rest_framework import serializers
from .models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'username','is_admin', 'is_receptionist', 'is_doctor',
                  'is_patient')

class DoctorsSerializer(serializers.ModelSerializer):
    user=UsersSerializer()
    class Meta:
        model = Doctors
        fields = ('user', 'especiality')
        
class PatientsSerializer(serializers.ModelSerializer):
    user=UsersSerializer()
    class Meta:
        model = Patients
        fields = ('user', 'birthdate', 'cpf', 'telephone', 'adress')

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('id','status_type','type','patient','doctor',  'date', 
                  'hour', 'is_active')
        
class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ('id','payment_type', 'value', 'appointment',
                  'doctor_value', 'clinic_value')


class AdminListSerializer(serializers.ModelSerializer):
    
    appointment = serializers.CharField(
        source='payments.appointment',
        read_only=True
        )
    
    date = serializers.DateField(
        source='payments.date',
        read_only=True
        )
    
    doctor = serializers.CharField(
        source='payments.appointment.doctor',
        read_only=True
        )
    
    patient = serializers.CharField(
        source='payments.appointment.patient',
        read_only=True
        )
    
    value = serializers.DecimalField(
        source='payments.value',
        read_only=True,
        max_digits=10,
        decimal_places=2
        )
    
    payment_type = serializers.CharField(
        source='payments.payment_type',
        read_only=True
        )
    
    class Meta:
        model = AdminList
        fields = ('appointment', 'date', 'doctor', 'patient',
                  'value', 'payment_type')
        
class DoctorListSerializer(serializers.ModelSerializer):
    
    patient = serializers.CharField(
        source='payments.appointment.patient',
        read_only=True
        )
    
    date = serializers.DateField(
        source='payments.date',
        read_only=True
        )
    
    value = serializers.DecimalField(
        source='payments.value',
        read_only=True,
        max_digits=10,
        decimal_places=2
        )
    
    doctor_value = serializers.DecimalField(
        source='payments.doctor_value',
        read_only=True,
        max_digits=10,
        decimal_places=2
        )
    
    class Meta:

        model = AdminList
        fields = ('patient', 'date', 'value', 'doctor_value')
        

