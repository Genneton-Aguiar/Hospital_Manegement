from ..repository.doctor_list_repository import DoctorListRepository

class DoctorListUseCase:
    def __init__(self, doctor_list_repository: DoctorListRepository):
        self.doctor_list_repository = doctor_list_repository

    def doctor_finance_list(self, current_user):
 
        if not current_user.is_authenticated or not current_user.is_doctor:
            raise PermissionError("Apenas DOC's podem visualizar esse relatório.")

        # Busca todos os pagamentos relacionados ao médico
        payments = self.doctor_list_repository.list_doctor_payments(current_user)
        if not payments.exists():
            raise ValueError("Nenhum pagamento encontrado para este médico.")
        
        report = []
        for payment in payments:
            report.append({
                'patient': payment.appointment.patient.user.username,
                'date': payment.appointment.date,
                'value': payment.value,
                'doctor_value': payment.doctor_value,
            })

        return report
    
    