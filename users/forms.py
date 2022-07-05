from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import CustomUser, Patient, Staff, Feedback, Emergency, Medicine, Prescription


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
    """
    class for creating prescription form
    """

    class Meta:
        model = Prescription
        fields = ['patient', 'medicine', 'count']

    def clean(self):
        cleaned_data = super().clean()
        fetch_medicine = cleaned_data.get("medicine")
        fetch_count = cleaned_data.get("count")
        query = Medicine.objects.filter(medicine_name=fetch_medicine)
        if not query:
            raise ValidationError(
                "You can not prescribe this medicine....please add the medicine first"
            )
        if fetch_count <= 0:
            raise ValidationError(
                "count can not be less than zero"
            )


class PrescriptionUpdateForm(forms.ModelForm):
    """
    This class is used to update fields of prescription.
    """

    class Meta:
        model = Prescription
        fields = ['medicine', 'count']

    def clean(self):
        cleaned_data = super().clean()
        fetch_medicine = cleaned_data.get("medicine")
        fetch_count = cleaned_data.get("count")
        query = Medicine.objects.filter(medicine_name=fetch_medicine)
        if not query:
            raise ValidationError(
                "You can not prescribe this medicine....please add the medicine first"
            )
        if fetch_count <=0:
            raise ValidationError(
                "count can not be less than zero"
            )


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
