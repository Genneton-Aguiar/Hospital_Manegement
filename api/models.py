from django.db import models
from django.contrib.auth.models import User

class Users(User):
    
    is_admin = models.BooleanField(
        verbose_name= 'administrador',
        default=False
    )
     
    is_receptionist = models.BooleanField(
        verbose_name= 'recepcionista',
        default=False
    )
    is_doctor = models.BooleanField(
        verbose_name= 'medico',
        default=False
    )
    is_patient = models.BooleanField(
        verbose_name= 'paciente',
        default=False
    )
    def __str__(self):
        return self.username
    

class Doctors(models.Model):
    
    user = models.OneToOneField(
        Users, 
        on_delete = models.DO_NOTHING,
        primary_key=True
    )
    
    especiality = models.CharField(
        verbose_name= 'especialidade',
        max_length=100
    )
    
    def __str__(self):
        return self.user.username


class Patients(models.Model):
    
    user = models.OneToOneField(
        Users, 
        on_delete = models.DO_NOTHING,
        primary_key=True
    )
    
    birthdate = models.DateField(
        verbose_name= 'nascimento',
        null=True
    )
    
    cpf= models.CharField(
        verbose_name= 'cpf',
        max_length=11, 
        null=True
    )
    
    telephone = models.CharField(
        verbose_name= 'telefone',
        max_length=11, 
        null=True
    )

    adress = models.CharField(
        verbose_name= 'endereço',
        max_length=255, 
        null=True
    )
    
    
    def __str__(self):
        return self.user.username


class Appointment(models.Model):
    
    AG = 'AGENDADO'
    REALIZADO = 'REALIZADO'
    CANCEL = 'CANCELADO'
    
    TYPE_CHOICES = [
        (AG, 'Agendado'),
        (REALIZADO, 'Realizado'),
        (CANCEL, 'Cancelado'),
    ]
    
    status_type = models.CharField(
        verbose_name = "status do agendamento", 
        max_length = 100,
        choices = TYPE_CHOICES,
        default = AG
    )
    
    type = models.CharField(
        verbose_name= 'tipo da consulta',
        max_length=100,
        null=True
    )
    
    patient = models.ForeignKey(
        Patients,
        verbose_name= 'paciente', 
        on_delete=models.DO_NOTHING,
        null=True
    )
    
    doctor = models.ForeignKey(
        Doctors,
        verbose_name= 'medico', 
        on_delete=models.DO_NOTHING,
        null=True
    )
    
    date = models.DateField(
        verbose_name='Data',
        null=True
    )
    
    hour = models.TimeField(
        verbose_name='Hora',
        null=True,
    )
    
    is_active = models.BooleanField(
        verbose_name= 'consulta ativa',
        default=True
    )
         
    def __str__(self):
        return f'{self.user} - {self.date}'
    

class Payments(models.Model):
    
    CARD = 'Cartão'
    MONEY = 'Dinheiro'
    TRANSF = 'Transferecia'
     
    TYPE_CHOICES = [
        (CARD, 'Cartão'),
        (MONEY, 'Dinheiro'),
        (TRANSF, 'Transferecia'),
    ]
    
    payment_type= models.CharField(
        verbose_name="Tipo de pagamento", 
        max_length=100,
        choices=TYPE_CHOICES,
        default=CARD
    )
    
    appointment = models.ForeignKey(
        Appointment, 
        on_delete=models.DO_NOTHING
        )
    
    value = models.FloatField(
        verbose_name= 'valor',
        null=True
    )
    
    doctor_value = models.FloatField(
        verbose_name= 'valor do médico',
        null=True
    )
    
    clinic_value = models.FloatField(
        verbose_name= 'valor da clínica',
        null=True
    )


    def __str__(self):
        return f'{self.user} - {self.appointment}'


class AdminList(models.Model):
    payment= models.ForeignKey(
        Payments, 
        on_delete=models.DO_NOTHING
        
    )
    def __str__(self):
        return f'{self.user} - {self.appointment}'
    
    
class DoctorList(models.Model):
    payment= models.ForeignKey(
        Payments, 
        on_delete=models.DO_NOTHING
        
    )
    def __str__(self):
        return f'{self.user} - {self.appointment}'
    
    