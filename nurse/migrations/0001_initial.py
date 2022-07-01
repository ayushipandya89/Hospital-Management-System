# Generated by Django 4.0.5 on 2022-07-01 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appointment', '0020_admit'),
        ('users', '0011_alter_customuser_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='NurseDuty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient', models.ManyToManyField(to='appointment.admit')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.staff')),
            ],
        ),
    ]
