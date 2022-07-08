import uuid
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


def validate_age(age):
    """
    function for age validation of users.
    """
    if age < 21:
        raise ValidationError('Please enter age above 21')


class UserRole(models.Model):
    """
    class for creating table of role in hospital
    """
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.role


class CustomUser(AbstractUser):
    """
    model for custom user table.
    """
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    ROLE_CHOICES = (
        ('D', 'Doctor'),
        ('P', 'Patient'),
        ('N', 'Nurse'),
    )
    email = models.EmailField(null=True)
    phone = PhoneNumberField(null=True, help_text='Please use following format for phone number: +917834442134')
    age = models.IntegerField(null=True, validators=[validate_age])
    address = models.CharField(max_length=300, null=True)
    profile = models.ImageField(default='default.jpg', upload_to='profile_pic/', null=True, blank=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, null=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, null=True)
    # role_fk = models.ForeignKey(UserRole,on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class StaffSpeciality(models.Model):
    """
    create class for adding speciality table for staff.
    """
    speciality = models.CharField(max_length=100)

    def __str__(self):
        return self.speciality


class Staff(models.Model):
    """
    class for creating staff tabl.
    """
    SPECIALITY_CHOICES = (
        ('MD Doctor', 'MD Doctor'),
        ('Pediatricians', 'Pediatricians'),
        ('Cardiologists', 'Cardiologists'),
        ('Neurologists', 'Neurologists'),
        ('surgeons', 'surgeons'),
        ('Orthopedic', 'Orthopedic'),
        ('Nurse', 'Nurse'),
    )
    staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    salary = models.IntegerField(default=0)
    is_approve = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)
    speciality = models.ForeignKey('StaffSpeciality', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.staff.username


class Patient(models.Model):
    """
    class for making patient table.
    """
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    UUID = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"UUID:{self.UUID} | Patient :{self.patient}"


class Feedback(models.Model):
    """
    class for user feedback.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)


class Prescription(models.Model):
    """
    class for creating table of patient's prescription
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    medicine = models.CharField(max_length=500)
    count = models.IntegerField()


class Emergency(models.Model):
    """
    class for creating emergency table
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now)
    disease = models.CharField(max_length=500)
    charge = models.DecimalField(max_digits=10, decimal_places=2)
    is_bill_generated = models.BooleanField(default=False)


class Medicine(models.Model):
    """
    class for creating table for medicine
    """
    medicine_name = models.CharField(max_length=200)
    charge = models.DecimalField(max_digits=10, decimal_places=2)


class Bill(models.Model):
    """
    class for creating bill table
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    staff_charge = models.DecimalField(max_digits=10, decimal_places=2)
    medicine_charge = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True)
    room_charge = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True)
    emergency_charge = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True)
    other_charge = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    total_charge = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
