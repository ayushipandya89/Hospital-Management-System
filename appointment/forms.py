from datetime import datetime

from django import forms

from appointment.models import Appointments
from users.models import Staff


class PatientAppointmentForm(forms.ModelForm):
    """
    for making appointment form
    """
    time_slot_choices = []
    time = datetime.now()
    current_time = time.strftime("%H:%M:%S")
    print(time, '-----------', time.hour)
    print(current_time.split(':')[0], '+++++++')
    query = Appointments.objects.all().values('timeslot')
    # y=query[0]
    print(query)
    for i in range(9, 20):
        if i > int(current_time.split(':')[0]):
            # y=query[0]
            # if i in query:
            #     print('nn')
            #
            # time_slot_choices.append((i, i))
            time_slot_choices.append((f"{i}:00", f"{i}:00"))
    print(time_slot_choices)

    timeslot = forms.ChoiceField(choices=time_slot_choices)

    class Meta:
        model = Appointments
        fields = ['staff', 'date', 'timeslot', 'disease']

    def __init__(self, *args, **kwargs):
        super(PatientAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['staff'].queryset = Staff.objects.filter(is_approve=True).filter(is_available=True)
