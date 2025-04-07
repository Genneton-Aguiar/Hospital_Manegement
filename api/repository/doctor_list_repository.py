from api.models import Payments

class DoctorListRepository:
    def list_doctor_payments(self, doctor):

        return Payments.objects.filter(appointment__doctor=doctor)

