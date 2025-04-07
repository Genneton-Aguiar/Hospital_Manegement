from ..repository.patient_repository import PatientRepository
from ..repository.user_repository import UserRepository

class PatientUseCase:
    def __init__(self, patient_repository: PatientRepository, user_repository: UserRepository):
        self.patient_repository = patient_repository
        self.user_repository = user_repository

    def list_patients(self, current_user):
        
        if not current_user.is_authenticated or not current_user.is_admin:
            raise PermissionError("Apenas ADM podem LISTAR pacientes.")
        
        return self.patient_repository.list_all_patients()

    def create_patient(self, data, current_user):
    
        if not current_user.is_authenticated or not current_user.is_admin:
            raise PermissionError("Apenas ADM podem CRIAR pacientes.")

        # Valida os dados recebidos
        username = data.get('username')
        password = data.get('password')
        birthdate = data.get('birthdate')
        cpf = data.get('cpf')
        telephone = data.get('telephone')
        address = data.get('address')

        if not username or not password or not cpf:
            raise ValueError("Username OU senha OU CPF esta vazio.")

        # Cria o usuário associado ao paciente
        user = self.user_repository.create_user(
            username=username,
            is_patient=True
        )

        # Cria o paciente no repositório
        return self.patient_repository.create_patient(
            user=user,
            birthdate=birthdate,
            cpf=cpf,
            telephone=telephone,
            address=address
        )

    def update_patient(self, patient_id, data, current_user):

        if not current_user.is_authenticated or not current_user.is_admin:
            raise PermissionError("Apenas administradores podem atualizar pacientes.")

        # Busca o paciente no repositório
        patient = self.patient_repository.get_patient_by_id(patient_id)
        if not patient:
            raise ValueError("Paciente não encontrado.")

        # Atualiza os dados do paciente
        return self.patient_repository.update_patient(patient, data)

    def delete_patient(self, patient_id, current_user):
 
        if not current_user.is_authenticated or not current_user.is_admin:
            raise PermissionError("Apenas administradores podem remover pacientes.")

        # Busca o paciente no repositório
        patient = self.patient_repository.get_patient_by_id(patient_id)
        if not patient:
            raise ValueError("Paciente não encontrado.")

        # Remove o paciente
        return self.patient_repository.delete_patient(patient)
    
    