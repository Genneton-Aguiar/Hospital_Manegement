from api.models import Patients
from django.db import transaction

class PatientRepository:
    def list_all_patients(self):
       
        return Patients.objects.all()

    def get_patient_by_id(self, patient_id):
   
        return Patients.objects.filter(pk=patient_id).first()

    def create_patient(self, user, birthdate, cpf, telephone, address):

        with transaction.atomic():
            patient = Patients.objects.create(
                user=user,
                birthdate=birthdate,
                cpf=cpf,
                telephone=telephone,
                address=address
            )
            return patient

    def update_patient(self, patient, data):
       
        for key, value in data.items():
            setattr(patient, key, value)
        patient.save()
        return patient

    def delete_patient(self, patient):
      
        patient.delete()
        return True
    