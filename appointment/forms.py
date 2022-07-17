from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError

from appointment.models import Appointments, Room, Admit
from users.models import Staff, CustomUser


class InputDate(forms.DateInput):
    input_type = 'date'


class PatientAppointmentForm(forms.ModelForm):
    """
    for making appointment form
    """
    timeslot = forms.ChoiceField()

    class Meta:
        model = Appointments
        fields = ['user', 'staff', 'date', 'disease', 'timeslot']
        widgets = {
            'date': InputDate()
        }

    def __init__(self, *args, **kwargs):
        super(PatientAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['timeslot'].queryset = Appointments.objects.none()

        if 'staff' in self.data:
            try:
                staff_id = int(self.data.get('staff'))
                self.fields['timeslot'].queryset = Appointments.objects.filter(staff_id=staff_id).order_by('staff_id')
            except(ValueError,TypeError):
                pass
        elif self.instance.pk:
            self.fields['timeslot'].queryset = self.instance.staff.timeslot_set.order_by('staff_id')


# class PatientAppointmentForm(forms.ModelForm):
#     """
#     for making appointment form
#     """
#
#     class Meta:
#         model = Appointments
#         fields = ['staff', 'date', 'disease']
#         widgets = {
#             'date': InputDate()
#         }
#
#     def __init__(self, *args, **kwargs):
#         super(PatientAppointmentForm, self).__init__(*args, **kwargs)
#         self.fields['staff'].queryset = Staff.objects.filter(is_approve=True).filter(is_available=True)
#
#     def clean(self):
#         cleaned_data = super().clean()
#         fetch_date = cleaned_data.get("date")
#         fetch_staff = cleaned_data.get("staff")
#         fetch_time = Appointments.objects.filter(date=fetch_date).filter(staff=fetch_staff).values('timeslot')
#         data = []
#         user_data = []
#         time_slot_choices = []
#         time = datetime.now()
#         date = datetime.now().date()
#         current_time = time.strftime("%H:%M:%S")
#         # for displaying the timeslot after the current time
#         for i in range(9, 20):
#             if i > int(current_time.split(':')[0]):
#                 if i != 12:
#                     user_data.append(i)
#                     time_slot_choices.append(f"{i}:00")
#         available_time = []
#         if int(current_time.split(':')[0]) >= 19:
#             raise ValidationError('The Hospital is close for today please choose another date or another staff')
#         else:
#             if fetch_date == date:
#                 # gathering the data of available choices
#                 for i in fetch_time:
#                     for j in i.values():
#                         available_time.append(j)
#                 # for comparing the available choices of timeslot
#                 result = all(elem in available_time for elem in time_slot_choices)
#                 if result:
#                     raise ValidationError('ALl slots are booked for today..Please choose another date')
#             else:
#                 if len(data) == 10:
#                     raise ValidationError('All slots of this date are booked..Please choose another date')
#
#
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
        if fetch_charge <= 0:
            raise ValidationError(
                "charge can not be less than zero"
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
        if fetch_charge <= 0:
            raise ValidationError(
                "charge can not be less than zero"
            )
