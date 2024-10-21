# Generated by Django 5.1.1 on 2024-10-11 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_doctors_patients_remove_users_adress_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_doctor',
            field=models.BooleanField(default=False, verbose_name='medico'),
        ),
        migrations.AddField(
            model_name='users',
            name='is_patient',
            field=models.BooleanField(default=False, verbose_name='paciente'),
        ),
    ]
