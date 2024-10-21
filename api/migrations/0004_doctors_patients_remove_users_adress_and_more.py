# Generated by Django 5.1.1 on 2024-10-11 14:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_payments_doctor_remove_appointment_doctor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctors',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='api.users')),
                ('especiality', models.CharField(max_length=100, verbose_name='especialidade')),
            ],
        ),
        migrations.CreateModel(
            name='Patients',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='api.users')),
                ('birthdate', models.DateField(null=True, verbose_name='nascimento')),
                ('cpf', models.CharField(max_length=11, null=True, verbose_name='cpf')),
                ('telephone', models.CharField(max_length=11, null=True, verbose_name='telefone')),
                ('adress', models.CharField(max_length=255, null=True, verbose_name='endereço')),
            ],
        ),
        migrations.RemoveField(
            model_name='users',
            name='adress',
        ),
        migrations.RemoveField(
            model_name='users',
            name='birthdate',
        ),
        migrations.RemoveField(
            model_name='users',
            name='cpf',
        ),
        migrations.RemoveField(
            model_name='users',
            name='is_doctor',
        ),
        migrations.RemoveField(
            model_name='users',
            name='is_patient',
        ),
        migrations.RemoveField(
            model_name='users',
            name='telephone',
        ),
    ]