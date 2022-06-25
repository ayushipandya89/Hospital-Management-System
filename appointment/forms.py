from django import forms
from appointment.models import Appointments


class PatientAppointmentForm(forms.ModelForm):
    """
    for making appointment form
    """

    class Meta:
        model = Appointments
        fields = ['staff', 'date', 'timeslot', 'disease']
