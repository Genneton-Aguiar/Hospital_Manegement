from django.test import TestCase
from api.models import Users
from api.repository.user_repository import UserRepository

class UserRepositoryTestCase(TestCase):
    def setUp(self):
        # Dados para o teste
        self.user_adm = Users.objects.create(
            username="admin", 
            is_admin=True, 
            is_active=True
            )
        
        self.user_receptionist = Users.objects.create(
            username="receptionist", 
            is_receptionist=True, 
            is_active=True
            )
        self.repository = UserRepository()

    def test_retorno_de_adm_e_recepcionista(self):

        users = self.repository.list_adm_recepcionist()
        self.assertEqual(len(users), 2)
        self.assertIn(self.user_adm, users)
        self.assertIn(self.user_receptionist, users)

    def test_retorno_por_id(self):
        
        user = self.repository.get_user_by_id(self.user_adm.id)
        self.assertEqual(user, self.user_adm)

    def test_create_user(self):
        
        user = self.repository.create_user(
            username="test_user", 
            password="senha123", 
            is_admin=False, 
            is_receptionist=True
            )
        self.assertEqual(user.username, "test_user")
        self.assertTrue(user.is_receptionist)
        self.assertFalse(user.is_admin)
    
    