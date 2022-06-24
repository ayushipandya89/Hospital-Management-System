import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


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
        ('W', 'Word-boy')
    )
    email = models.EmailField(null=True)
    phone = PhoneNumberField(null=True, help_text='Please use following format for phone number: +917834442134')
    age = models.IntegerField(null=True)
    address = models.CharField(max_length=300, null=True)
    profile = models.ImageField(default='default.jpg', upload_to='profile_pic/', null=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, null=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, null=True)

    def __str__(self):
        return self.username


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
    speciality = models.CharField(max_length=50, choices=SPECIALITY_CHOICES)

    def __str__(self):
        return self.staff.username


class Patient(models.Model):
    """
    class for making patient table.
    """
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    UUID = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.UUID)
