from api.models import Users
from django.db import transaction
from django.db.models import Q


class UserRepository:   
    def list_adm_recepcionist(self):
        return Users.objects.filter(
            Q(is_admin=True) | Q(is_receptionist=True),
            is_active=True
        )
        
    def get_user_by_id(self, user_id):
        return Users.objects.filter(pk=user_id).first()

    def create_user(self, username, password, is_admin=False, is_receptionist=False):
        with transaction.atomic():
            user = Users.objects.create(
                username=username,
                is_admin=is_admin,
                is_receptionist=is_receptionist,
            )
            user.set_password(password)
            user.save()
            return user

    def update_user(self, user, data):
        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return user

    def delete_user(self, user):
        user.is_active = False
        user.save()
        return user

