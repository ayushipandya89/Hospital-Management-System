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

    def clean(self):
        cleaned_data = super().clean()
        fetch_date = cleaned_data.get("date")
        fetch_time = Appointments.objects.filter(date=fetch_date).values('timeslot')
        data = []
        user_data = []
        time_slot_choices = []
        time = datetime.now()
        date = datetime.now().date()
        current_time = time.strftime("%H:%M:%S")
        # for displaying the timeslot after the current time
        for i in range(9, 20):
            if i > int(current_time.split(':')[0]):
                if i != 12:
                    user_data.append(i)
                    time_slot_choices.append(f"{i}:00")
        available_time = []
        if int(current_time.split(':')[0]) >= 19:
            raise ValidationError('The Hospital is close for today please choose another date')
        else:
            if fetch_date == date:
                # gathering the data of available choices
                for i in fetch_time:
                    for j in i.values():
                        available_time.append(j)
                # for comparing the available choices of timeslot
                result = all(elem in available_time for elem in time_slot_choices)
                if result:
                    raise ValidationError('ALl slots are booked for today..Please choose another date')
            else:
                if len(data) == 10:
                    raise ValidationError('All slots of this date are booked..Please choose another date')


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
        time_query = Appointments.objects.all().filter(date=date_query).filter(timeslot=fetch_time).filter(
            staff=staff_query)
        if time_query:
            raise ValidationError('This slot is already booked please choose another slot')
