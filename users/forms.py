from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from appointment.models import Appointments, Admit
from .models import CustomUser, Patient, Staff, Feedback, Emergency, Medicine, Prescription, Bill, UserRole, \
    StaffSpeciality


class UserRegisterForm(UserCreationForm):
    """
    This class adds the custom fields to  registration form.
    """

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'age', 'address', 'gender', 'role', 'password1', 'password2', 'profile']

    def clean(self):
        cleaned_data = super().clean()
        fetch_age = cleaned_data.get("age")

        if int(fetch_age) < 21:
            raise ValidationError(
                "age can not be less than 21"
            )


class AddRoleForm(forms.ModelForm):
    """
    class for creating form for adding role in the table
    """

    class Meta:
        model = UserRole
        fields = ['role']


class UserUpdateForm(forms.ModelForm):
    """
    This class is used to update fields of custom user.
    """

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'age', 'gender', 'address', 'profile']

    def clean(self):
        cleaned_data = super().clean()
        fetch_age = cleaned_data.get("age")

        if int(fetch_age) < 21:
            raise ValidationError(
                "age can not be less than 21"
            )


class PatientRegistrationForm(forms.ModelForm):
    """
    This class adds the data to patient table.
    """

    class Meta:
        model = Patient
        fields = ['patient']


class AddSpecialityForm(forms.ModelForm):
    """
    class for creating form for adding speciality
    """

    class Meta:
        model = StaffSpeciality
        fields = ['speciality']


class StaffUpdateForm(forms.ModelForm):
    """
    This class is used to update fields of custom user.
    """

    class Meta:
        model = Staff
        fields = ['salary', 'speciality', 'is_approve', 'is_available']


class FeedbackForm(forms.ModelForm):
    """
    class for creating feedback form for user.
    """

    class Meta:
        model = Feedback
        fields = ['content']


class PrescriptionForm(forms.ModelForm):
    patient = forms.ModelChoiceField(queryset=None)
    staff = forms.ModelChoiceField(queryset=None)
    medicine = forms.CharField()
    count = forms.IntegerField()

    class Meta:
        model = Prescription
        fields = ['patient', 'staff', 'medicine', 'count']

    def __init__(self, *args, **kwargs):
        super(PrescriptionForm, self).__init__(*args, **kwargs)
        self.fields['patient'].queryset = Admit.objects.filter(out_date__isnull=True)
        self.fields['staff'].queryset = Staff.objects.filter(is_approve=True).filter(is_available=True)

    def clean(self):
        cleaned_data = super().clean()
        a = Patient.objects.filter(patient__username=cleaned_data['patient']).first()
        print('query fetching patient name: ', a)
        cleaned_data['patient'] = a
        fetch_count = cleaned_data.get("count")
        if fetch_count <= 0:
            self._errors["count"] = ["count can npt be less than zero"]


class PrescriptionUpdateForm(forms.ModelForm):
    """
    This class is used to update fields of prescription.
    """
    count = forms.IntegerField()

    class Meta:
        model = Prescription
        fields = ['medicine']

    def clean(self):
        cleaned_data = super().clean()
        fetch_medicine = cleaned_data.get("medicine")
        # fetch_count = cleaned_data.get("count")
        query = Medicine.objects.filter(medicine_name=fetch_medicine)
        if not query:
            raise ValidationError(
                "You can not prescribe this medicine....please add the medicine first"
            )
        # if fetch_count <= 0:
        #     raise ValidationError(
        #         "count can not be less than zero"
        #     )


class EmergencyForm(forms.ModelForm):
    """
    This class is used for emergency cases forms.
    """

    class Meta:
        model = Emergency
        fields = ['patient', 'staff', 'datetime', 'disease', 'charge']

    def __init__(self, *args, **kwargs):
        super(EmergencyForm, self).__init__(*args, **kwargs)
        self.fields['staff'].queryset = Staff.objects.filter(is_approve=True).filter(is_available=True)

    def clean(self):
        cleaned_data = super().clean()
        fetch_charge = cleaned_data.get("charge")
        if fetch_charge < 500:
            raise ValidationError(
                "Emergency charge can not be less than 500"
            )


class MedicineForm(forms.ModelForm):
    """
    class for creating form for adding medicine
    """

    class Meta:
        model = Medicine
        fields = ['medicine_name', 'charge']


class MedicineUpdateForm(forms.ModelForm):
    """
    This class is used to update fields of medicine table.
    """

    class Meta:
        model = Medicine
        fields = ['medicine_name', 'charge']


class CreateBillForm(forms.ModelForm):
    """
    class for generating form for bill
    """

    class Meta:
        model = Bill
        fields = ['patient', 'staff_charge', 'other_charge']

    def __init__(self, *args, **kwargs):
        super(CreateBillForm, self).__init__(*args, **kwargs)
        admit_query = Admit.objects.values('patient__patient__username', 'patient__id')
        appointment_query = Appointments.objects.values('user__username', 'user__patient__id')
        emergency_query = Emergency.objects.values('patient__patient__username', 'patient__id')
        fetch_patient = []
        for element in admit_query.union(appointment_query, emergency_query):
            fetch_patient.append((element.get('patient__id'), element.get('patient__patient__username')))
        print(fetch_patient)
        self.fields['patient'] = forms.ChoiceField(choices=fetch_patient)

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['patient'] = Patient.objects.filter(id=cleaned_data['patient']).first()
        fetch_staff_charge = cleaned_data.get("staff_charge")
        bill_generated_already = Bill.objects.filter(patient=cleaned_data['patient'])
        not_discharge = Admit.objects.filter(patient=cleaned_data['patient']).first()
        # print('out date: ',not_discharge.out_date)
        # print('not_discharge',not_discharge)
        # print('bill_generated_already',bill_generated_already)
        print(not_discharge)
        if not_discharge:
            if not not_discharge.out_date:
                raise ValidationError(
                    "This patient is not discharged yet..."
                )
        if bill_generated_already:
            raise ValidationError(
                "Bill of this patient is already generated please choose another patient"
            )
        if fetch_staff_charge < 500:
            raise ValidationError(
                "charge can not be less than 500"
            )
