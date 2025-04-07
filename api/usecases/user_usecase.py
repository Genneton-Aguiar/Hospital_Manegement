from ..repository.user_repository import UserRepository

class UserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def list_users(self, current_user):
        
        if not current_user.is_authenticated or not current_user.is_admin:
            raise PermissionError("Apenas ADM pode LISTAR usuários.")
        
        return self.user_repository.list_adm_recepcionist()

    def create_user(self, data, current_user, request):
        
        if not current_user.is_authenticated or not current_user.is_admin:
            raise PermissionError("Apenas ADM pode LISTAR usuários.") 
        data = request.data
        if not data:
            raise ValueError("Informe os dados do usuário.")
        
        username = data.get('username')
        password = data.get('password')
        is_admin = data.get('is_admin', False)
        is_receptionist = data.get('is_receptionist', False)

        if not username or not password:
            raise ValueError("Informe o username ou a senha.")
        

        return self.user_repository.create_user(
            username=username,
            password=password,
            is_admin=is_admin,
            is_receptionist=is_receptionist,
        )
                                                                                                                                        
    def update_user(self, user_id, data, current_user):
        
        if not current_user.is_authenticated or not current_user.is_admin:
            raise PermissionError("Apenas ADM pode EDITAR usuários.")
        
        
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado.")
        return self.user_repository.update_user(user, data)

    def delete_user(self, user_id, current_user):
        if not current_user.is_authenticated or not current_user.is_admin:
            raise PermissionError("Apenas ADM pode DELETAR usuários.")
        
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado.")
        return self.user_repository.deactivate_user(user)
    
    