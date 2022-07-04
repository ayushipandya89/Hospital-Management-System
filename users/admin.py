from django.contrib import admin

from .models import CustomUser, Patient, Staff, Feedback, Prescription, Emergency

admin.site.register(CustomUser)
admin.site.register(Staff)
admin.site.register(Patient)
admin.site.register(Feedback)
admin.site.register(Prescription)
admin.site.register(Emergency)

