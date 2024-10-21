from django.contrib import admin
from .models import *


admin.site.register(Users)
admin.site.register(Doctors)
admin.site.register(Patients)
admin.site.register(Appointment)
admin.site.register(Payments)
admin.site.register(AdminList)  
admin.site.register(DoctorList)
