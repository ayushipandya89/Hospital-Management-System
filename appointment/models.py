from django.db import models
from users.models import CustomUser, Staff


class Appointments(models.Model):
    DEPARTMENT_CHOICE = (
        ('MD Doctor', 'MD Doctor'),
        ('Pediatricians', 'Pediatricians'),
        ('Cardiologists', 'Cardiologists'),
        ('Neurologists', 'Neurologists'),
        ('surgeons', 'surgeons'),
        ('Orthopedic', 'Orthopedic'),
    )
    TIMESLOT_LIST = (
        ('09:00 – 09:30', '09:00 – 09:30'),
        ('10:00 – 10:30', '10:00 – 10:30'),
        ('11:00 – 11:30', '11:00 – 11:30'),
        ('12:00 – 12:30', '12:00 – 12:30'),
        ('13:00 – 13:30', '13:00 – 13:30'),
        ('14:00 – 14:30', '14:00 – 14:30'),
        ('15:00 – 15:30', '15:00 – 15:30'),
        ('16:00 – 16:30', '16:00 – 16:30'),
        ('17:00 – 17:30', '17:00 – 17:30'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField(help_text="Use that Format:YYYY-MM-DD...For example: 2022/6/26")
    timeslot = models.CharField(max_length=100, choices=TIMESLOT_LIST)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICE)
    disease = models.CharField(max_length=300)

    def __str__(self):
        return f"Patient: {self.user} | Time: {self.timeslot}"

    @property
    def time(self):
        return self.TIMESLOT_LIST[self.timeslot][1]
