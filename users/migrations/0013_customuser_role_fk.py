# Generated by Django 4.0.5 on 2022-07-08 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_userrole'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.userrole'),
        ),
    ]
