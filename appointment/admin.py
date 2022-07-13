from django.contrib import admin
from .models import Appointments, Room, Admit, AdmitStaff

admin.site.register(Appointments)
admin.site.register(Room)
admin.site.register(Admit)
admin.site.register(AdmitStaff)

