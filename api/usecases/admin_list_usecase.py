from ..repository.admin_list_repository import AdminListRepository

class AdminListUseCase:
    def __init__(self, admin_list_repository: AdminListRepository):
        self.admin_list_repository = admin_list_repository

    def admin_finance_list (self, current_user):
        
        if not current_user.is_authenticated or not current_user.is_admin:
            raise PermissionError("Apenas ADM pode visualizar relatórios financeiros.")

        # Busca todos os pagamentos
        payments = self.admin_list_repository.list_admin_payments()

        finance_list = []
        for payment in payments:
            finance_list.append({
                'appointment': payment.appointment.id,
                'date': payment.appointment.date,
                'doctor': payment.appointment.doctor.user.username,
                'patient': payment.appointment.patient.user.username,
                'value': payment.value,
                'payment_type': payment.payment_type
            })

        return finance_list
    