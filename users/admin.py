from django.contrib import admin
from .models import CustomUser, Patient, Staff

admin.site.register(CustomUser)
admin.site.register(Staff)
admin.site.register(Patient)
