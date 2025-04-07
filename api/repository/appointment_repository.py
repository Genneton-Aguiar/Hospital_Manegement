from api.models import Appointment
from django.db import transaction

class AppointmentRepository:
    def list_all_appointments(self):
        """Retorna todas as consultas."""
        return Appointment.objects.all()

    def get_appointment_by_id(self, appointment_id):
        """Busca uma consulta pelo ID."""
        return Appointment.objects.filter(pk=appointment_id).first()
    
    def get_appointments_by_status(self, status_type):
        """Busca consultas pelo status."""
        return Appointment.objects.filter(status_type=status_type)
    
    def create_appointment(self, type, patient, doctor, date, hour, status_type):
        """Cria uma nova consulta."""
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
        """Atualiza os dados de uma consulta."""
        for key, value in data.items():
            setattr(appointment, key, value)
        appointment.save()
        return appointment

    def deactivate_appointment(self, appointment):
        """Desativa uma consulta."""
        appointment.is_active = False
        appointment.save()
        return appointment