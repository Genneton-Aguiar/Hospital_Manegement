from .models import *
from .serializer import *
from requests import request

from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
)


def create_users(data):
    
    username=data.get('username')
    password= data.get('password')
    is_admin= data.get('is_admin')
    
    is_receptionist= data.get('is_receptionist')


    users = Users.objects.create(
        username=username, 
        is_admin=is_admin,
        is_receptionist=is_receptionist,
        )
    
    
    users.set_password(password)
    users.save()
    
    return users


def create_doctor(data):
    
    username = data.get('username')
    password = data.get('password')
    especiality = data.get('especiality')

    user = Users.objects.create(username=username ,is_doctor=True)
    user.set_password(password)
    user.save()

    doctor = Doctors.objects.create(
        user=user, 
        especiality=especiality
        )
    
    return doctor


def create_patients(data):

    username = data.get('username')
    password = data.get('password')
    birthdate = data.get('birthdate')
    cpf = data.get('cpf')
    telephone = data.get('telephone')
    adress= data.get('adress')

    user = Users.objects.create(
        username=username, 
        is_patient=True
        )
    
    user.set_password(password)
    user.save()

    patients = Patients.objects.create(
        user=user, 
        birthdate=birthdate,
        cpf=cpf,
        telephone=telephone,
        adress=adress,
        )
    
    return patients

