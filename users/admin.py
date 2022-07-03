from django.contrib import admin

from .models import CustomUser, Patient, Staff, Feedback

admin.site.register(CustomUser)
admin.site.register(Staff)
admin.site.register(Patient)
admin.site.register(Feedback)

