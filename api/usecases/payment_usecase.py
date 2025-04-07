from ..repository.payment_repository import PaymentRepository
from ..repository.appointment_repository import AppointmentRepository

class PaymentUseCase:
    def __init__(self, payment_repository: PaymentRepository, appointment_repository: AppointmentRepository):
        self.payment_repository = payment_repository
        self.appointment_repository = appointment_repository

    def list_payments(self, current_user):
        
        if not current_user.is_authenticated or not current_user.is_admin:
            raise PermissionError("Apenas ADM pode LISTAR pagamentos.")
        
        return self.payment_repository.list_all_payments()

    def create_payment(self, data, current_user):
        
        if not current_user.is_authenticated or not current_user.is_admin:
            raise PermissionError("Apenas ADM pode CRIAR pagamentos.")

        
        appointment_id = data.get('appointment')
        appointment = self.appointment_repository.get_appointment_by_id(appointment_id)
        if not appointment:
            raise ValueError("ID da consulta incorreto ou inexistente.") 
        
        value = float(data.get('value', 0))
        payment_type = data.get('payment_type')

        if not appointment_id or not value or not payment_type:
            raise ValueError("Todos os campos devem ser preenchidos.")
        

        # repasse dos medicos
        doctor_value = value * 0.7
        clinic_value = value * 0.3

        # Cria o pagamento no repositório
        payment = self.payment_repository.create_payment(
            appointment=appointment,
            value=value,
            payment_type=payment_type,
            doctor_value=doctor_value,
            clinic_value=clinic_value
        )

        # Atualiza o status da consulta
        appointment.is_active = False
        appointment.save()

        return payment

