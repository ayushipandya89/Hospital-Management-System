from datetime import datetime

from django import forms

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

    # def clean(self):
    #     cleaned_data = super().clean()
    #     fetch_date = cleaned_data.get('date')
    #     print(fetch_date)
    #     fetch_timeslot = cleaned_data.get('timeslot')
    #     print(fetch_timeslot)
    #     query = Appointments.objects.all().values('date','timeslot')
    #     print(query)


class PatientTimeslotsUpdate(forms.ModelForm):
    """
    class for taking timeslot for appointment
    """

    time_slot_choices = []
    date = datetime.now().date()
    # print(date,'/////////')
    # if
    time = datetime.now()
    current_time = time.strftime("%H:%M:%S")
    # print(time, '-----------', time.hour)
    # print(current_time.split(':')[0], '+++++++')
    query = Appointments.objects.all().values('timeslot')
    # print(query)
    for i in range(9, 20):
        if i > int(current_time.split(':')[0]):
            if i != 12:
                time_slot_choices.append((f"{i}:00", f"{i}:00"))
    # print(time_slot_choices)
    query = Appointments.objects.all().values('date','timeslot')
    date_list = []
    # for d in query:
    #     for key in d.keys():
    #         print(d[key])
    #         date_list.append(d[key])
    # print(date_list)
    timeslot = forms.ChoiceField(choices=time_slot_choices)

    class Meta:
        model = Appointments
        fields = ['timeslot']
