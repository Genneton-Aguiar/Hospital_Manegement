from api.models import Appointment
from django.db import transaction

class AppointmentRepository:
    def list_all_appointments(self):
      
        return Appointment.objects.all()

    def get_appointment_by_id(self, appointment_id):
       
        return Appointment.objects.filter(pk=appointment_id).first()
    
    def get_appointments_by_status(self, status_type):
    
        return Appointment.objects.filter(status_type=status_type)
    
    def create_appointment(self, type, patient, doctor, date, hour, status_type):
        
        with transaction.atomic():
            appointment = Appointment.objects.create(
                type=type,
                patient=patient,
                doctor=doctor,
                date=date,
                hour=hour,
                status_type=status_type
            )
            return appointment

    def update_appointment(self, appointment, data):
        
        for key, value in data.items():
            setattr(appointment, key, value)
        appointment.save()
        return appointment

    def deactivate_appointment(self, appointment):
  
        appointment.is_active = False
        appointment.save()
        return appointment
    