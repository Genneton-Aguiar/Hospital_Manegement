from ..repository.doctor_repository import DoctorRepository
from ..repository.user_repository import UserRepository

class DoctorUseCase:
    def __init__(self, doctor_repository: DoctorRepository, user_repository: UserRepository):
        self.doctor_repository = doctor_repository
        self.user_repository = user_repository

    def list_doctors(self):
        """Lista todos os médicos."""
        return self.doctor_repository.list_all_doctors()

    def create_doctor(self, data, current_user):
        """Cria um novo médico."""
        if not current_user.is_authenticated or not current_user.is_admin:
            raise PermissionError("Apenas administradores podem criar médicos.")

        # Valida os dados recebidos
        username = data.get('username')
        password = data.get('password')
        especiality = data.get('especiality')

        if not username or not password:
            raise ValueError("Username e password são obrigatórios.")

        # Cria o usuário associado ao médico na aba de usuários
        user = self.user_repository.create_user(
            username=username,
            is_doctor=True,
        )

        # Cria o médico no repositório de doctors
        return self.doctor_repository.create_doctor(
            user=user, 
            especiality=especiality
            )

    def update_doctor(self, doctor_id, data, current_user):
        """Atualiza os dados de um médico."""
        if not current_user.is_authenticated or not current_user.is_admin:
            raise PermissionError("Apenas administradores podem atualizar médicos.")

        # Busca o médico no repositório
        doctor = self.doctor_repository.get_doctor_by_id(doctor_id)
        if not doctor:
            raise ValueError("Médico não encontrado.")

        # Atualiza os dados do médico
        return self.doctor_repository.update_doctor(doctor, data)

    def delete_doctor(self, doctor_id, current_user):
        """Remove um médico."""
        if not current_user.is_authenticated or not current_user.is_admin:
            raise PermissionError("Apenas administradores podem remover médicos.")

        # Busca o médico no repositório
        doctor = self.doctor_repository.get_doctor_by_id(doctor_id)
        if not doctor:
            raise ValueError("Médico não encontrado.")

        # Remove o médico
        return self.doctor_repository.delete_doctor(doctor)