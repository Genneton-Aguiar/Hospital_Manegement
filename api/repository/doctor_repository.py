from api.models import Doctors
from django.db import transaction

class DoctorRepository:
    def list_all_doctors(self):
      
        return Doctors.objects.all()

    def get_doctor_by_id(self, doctor_id):
        
        return Doctors.objects.filter(pk=doctor_id).first()

    def create_doctor(self, user, especiality):
  
        with transaction.atomic():
            doctor = Doctors.objects.create(
                user=user,
                especiality=especiality
            )
            return doctor

    def update_doctor(self, doctor, data):
     
        for key, value in data.items():
            setattr(doctor, key, value)
        doctor.save()
        return doctor

    def delete_doctor(self, doctor):
   
        doctor.delete()
        return True