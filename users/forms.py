from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import CustomUser, Patient


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


class PatientRegistrationForm(forms.ModelForm):
    """
    This class adds the data to patient table.
    """

    class Meta:
        model = Patient
        fields = ['patient']
