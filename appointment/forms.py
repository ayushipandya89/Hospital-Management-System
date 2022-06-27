from django import forms
from appointment.models import Appointments
from users.models import Staff


class PatientAppointmentForm(forms.ModelForm):
    """
    for making appointment form
    """

    timeslot = forms.CharField()

    class Meta:
        model = Appointments
        fields = ['staff', 'date', 'timeslot', 'disease']

    def __init__(self, *args, **kwargs):
        super(PatientAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['staff'].queryset = Staff.objects.filter(is_approve=True).filter(is_available=True)

    # def __init__(self, user, *args, **kwargs):
    #     super(PatientAppointmentForm, self).__init__(*args, **kwargs)
    #     self.fields['timeslot'] = forms.CharField(max_length=200
    #         # choices=[(o.id, str(o)) for o in Waypoint.objects.filter(user=user)]
    #     )