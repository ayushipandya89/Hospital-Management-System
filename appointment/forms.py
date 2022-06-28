from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError

from appointment.models import Appointments
from users.models import Staff


class PatientAppointmentForm(forms.ModelForm):
    """
    for making appointment form
    """

    class Meta:
        model = Appointments
        fields = ['staff', 'date', 'disease']

    def __init__(self, *args, **kwargs):
        super(PatientAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['staff'].queryset = Staff.objects.filter(is_approve=True).filter(is_available=True)


class PatientTimeslotsUpdate(forms.ModelForm):
    """
    class for taking timeslot for appointment
    """

    time_slot_choices = []
    date = datetime.now().date()
    time = datetime.now()
    current_time = time.strftime("%H:%M:%S")
    date_query = Appointments.objects.last().date
    if date_query == date:
        for i in range(9, 20):
            if i > int(current_time.split(':')[0]):
                if i != 12:
                    time_slot_choices.append((f"{i}:00", f"{i}:00"))
    else:
        for i in range(9, 20):
            if i != 12:
                time_slot_choices.append((f"{i}:00", f"{i}:00"))
    timeslot = forms.ChoiceField(choices=time_slot_choices)

    class Meta:
        model = Appointments
        fields = ['timeslot']

    def clean(self):
        cleaned_data = super().clean()
        fetch_time = cleaned_data.get("timeslot")
        date_query = Appointments.objects.last().date
        staff_query = Appointments.objects.last().staff
        time_query = Appointments.objects.all().filter(date=date_query).filter(timeslot=fetch_time).filter(staff=staff_query)
        if time_query:
            raise ValidationError('This slot is already booked please choose another slot')
