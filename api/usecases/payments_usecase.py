from ..repository.payment_repository import PaymentRepository
from ..repository.appointment_repository import AppointmentRepository

class PaymentUseCase:
    def __init__(self, payment_repository: PaymentRepository, appointment_repository: AppointmentRepository):
        self.payment_repository = payment_repository
        self.appointment_repository = appointment_repository

    def list_payments(self):
        """Lista todos os pagamentos."""
        return self.payment_repository.list_all_payments()

    def create_payment(self, data, current_user):
        """Cria um novo pagamento."""
        if not current_user.is_authenticated or not current_user.is_admin:
            raise PermissionError("Apenas administradores podem criar pagamentos.")

        # Valida os dados recebidos
        appointment_id = data.get('appointment')
        value = float(data.get('value', 0))
        payment_type = data.get('payment_type')

        if not appointment_id or not value or not payment_type:
            raise ValueError("Todos os campos obrigatórios devem ser preenchidos.")

        # Busca a consulta associada ao pagamento
        appointment = self.appointment_repository.get_appointment_by_id(appointment_id)
        if not appointment:
            raise ValueError("Consulta não encontrada.")

        # Calcula os valores para o médico e a clínica
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

    def delete_payment(self, payment_id, current_user):
        """Remove um pagamento."""
        if not current_user.is_authenticated or not current_user.is_admin:
            raise PermissionError("Apenas administradores podem remover pagamentos.")

        # Busca o pagamento no repositório
        payment = self.payment_repository.get_payment_by_id(payment_id)
        if not payment:
            raise ValueError("Pagamento não encontrado.")

        # Remove o pagamento
        return self.payment_repository.delete_payment(payment)