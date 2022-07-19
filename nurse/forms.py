from django import forms

from appointment.models import Admit
from nurse.models import NurseDuty
from users.models import Staff


class DutyForm(forms.ModelForm):
    """
    used for creating form to assign the duty of nurses.
    """

    class Meta:
        model = NurseDuty
        fields = ['staff', 'patient']

    def __init__(self, *args, **kwargs):
        super(DutyForm, self).__init__(*args, **kwargs)
        self.fields["staff"].queryset = Staff.objects.filter(speciality__speciality='Nurse').filter(is_approve=True).filter(
            is_available=True)
        self.fields["patient"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["patient"].queryset = Admit.objects.values_list('patient', flat=True)
        self.fields["patient"].queryset = Admit.objects.all().filter(out_date__isnull=True)
        # self.fields["patient"].queryset = Admit.objects.filter(out_date__isnull=True).values_list('pk', flat=True)
