from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError

from appointment.models import Appointments, Room, Admit
from users.models import Staff, CustomUser


class InputDate(forms.DateInput):
    input_type = 'date'


class CustomChoiceField(forms.ChoiceField):

    def validate(self, value):
        return value


class PatientAppointmentForm(forms.ModelForm):
    """
    for making appointment form
    """
    timeslot = CustomChoiceField()

    class Meta:
        model = Appointments
        fields = ['staff', 'date', 'disease', 'timeslot']
        widgets = {
            'date': InputDate()
        }


class PatientTimeslotsUpdate(forms.ModelForm):
    """
    class for taking timeslot for appointment
    """

    time_slot_choices = []
    date = datetime.now().date()
    time = datetime.now()
    current_time = time.strftime("%H:%M:%S")
    date_query = Appointments.objects.last()
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


class CreateRoomForm(forms.ModelForm):
    """
    class for entering the rooms date
    """
    fetch_admin = CustomUser.objects.filter(is_superuser=True)
    if not fetch_admin:
        raise ValidationError('You are not admin you can not edit this form')

    class Meta:
        model = Room
        fields = ['charge', 'AC', 'is_ICU', 'room_type']

    def clean(self):
        cleaned_data = super().clean()
        fetch_charge = cleaned_data.get("charge")
        print(fetch_charge)
        if fetch_charge < 500:
            raise ValidationError(
                "charge can not be less than 500 rupees"
            )


class AdmitPatientForm(forms.ModelForm):
    """
    class for creating form for admitted patient
    """

    class Meta:
        model = Admit
        fields = ['room', 'patient', 'disease', 'in_date', 'staff']
        widgets = {
            'in_date': InputDate()
        }

    def __init__(self, *args, **kwargs):
        super(AdmitPatientForm, self).__init__(*args, **kwargs)
        self.fields["staff"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["staff"].queryset = Staff.objects.filter(is_approve=True).filter(is_available=True)


class DischargeUpdateForm(forms.ModelForm):
    """
    This class is used to discharge patient form
    """

    class Meta:
        model = Admit
        fields = ['out_date', 'charge']
        widgets = {
            'out_date': InputDate()
        }

    def clean(self):
        cleaned_data = super().clean()
        fetch_charge = cleaned_data.get("charge")
        print(fetch_charge)
        if fetch_charge < 500:
            raise ValidationError(
                "charge can not be less 500"
            )
