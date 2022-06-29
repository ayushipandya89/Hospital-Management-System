from django.contrib import admin

from appointment.models import Admit, AdmitMapping
from .models import CustomUser, Patient, Staff

admin.site.register(CustomUser)
admin.site.register(Staff)
admin.site.register(Patient)
admin.site.register(Admit)
admin.site.register(AdmitMapping)

