from api.models import Payments

class AdminListRepository:
    def list_admin_payments(self):
        
        return Payments.objects.all()
    