from django.contrib import admin

from .models import CustomUser, Patient, Staff, Feedback, Prescription

admin.site.register(CustomUser)
admin.site.register(Staff)
admin.site.register(Patient)
admin.site.register(Feedback)
admin.site.register(Prescription)

