from ..repository.appointment_repository import AppointmentRepository
from ..repository.patient_repository import PatientRepository
from ..repository.doctor_repository import DoctorRepository

class AppointmentUseCase:
    def __init__(self, appointment_repository: AppointmentRepository, patient_repository: PatientRepository, doctor_repository: DoctorRepository):
        self.appointment_repository = appointment_repository
        self.patient_repository = patient_repository
        self.doctor_repository = doctor_repository

    def list_appointments(self, status_type=None):
        """Lista todas as consultas, com filtro opcional por status."""
        appointments = self.appointment_repository.list_all_appointments()
        
        if status_type:
            appointments = self.appointment_repository.list_appointments_by_status(status_type)
        return appointments

    def create_appointment(self, data, current_user):
        """Cria uma nova consulta."""
        if not current_user.is_authenticated or not (current_user.is_receptionist or current_user.is_doctor):
            raise PermissionError("Apenas recepcionistas ou médicos podem criar consultas.")

        # Valida os dados recebidos
        type = data.get('type')
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        date = data.get('date')
        hour = data.get('hour')
        status_type = data.get('status_type')

        if not type or not patient_id or not doctor_id or not date or not hour:
            raise ValueError("Todos os campos obrigatórios devem ser preenchidos.")

        # Busca o paciente e o médico
        patient = self.patient_repository.get_patient_by_id(patient_id)
        doctor = self.doctor_repository.get_doctor_by_id(doctor_id)

        if not patient:
            raise ValueError("Paciente não encontrado.")
        if not doctor:
            raise ValueError("Médico não encontrado.")

        # Verifica conflitos de horário
        conflicting_appointments = self.appointment_repository.list_all_appointments().filter(
            doctor=doctor,
            date=date,
            hour=hour
        ).exists()

        if conflicting_appointments == True:
            raise ValueError("Este médico já tem uma consulta agendada neste horário.")

        # Cria a consulta
        return self.appointment_repository.create_appointment(
            type=type,
            patient=patient,
            doctor=doctor,
            date=date,
            hour=hour,
            status_type=status_type
        )

    def update_appointment(self, appointment_id, data, current_user):
        """Atualiza os dados de uma consulta."""
        if not current_user.is_authenticated or not current_user.is_doctor:
            raise PermissionError("Apenas médicos podem atualizar consultas.")

        # Busca a consulta no repositório
        appointment = self.appointment_repository.get_appointment_by_id(appointment_id)
        if not appointment:
            raise ValueError("Consulta não encontrada.")

        # Atualiza os dados da consulta
        return self.appointment_repository.update_appointment(appointment, data)

    def deactivate_appointment(self, appointment_id, current_user):
        """Desativa uma consulta."""
        if not current_user.is_authenticated or not current_user.is_receptionist:
            raise PermissionError("Apenas recepcionistas podem desativar consultas.")

        # Busca a consulta no repositório
        appointment = self.appointment_repository.get_appointment_by_id(appointment_id)
        if not appointment:
            raise ValueError("Consulta não encontrada.")

        # Desativa a consulta
        return self.appointment_repository.deactivate_appointment(appointment)