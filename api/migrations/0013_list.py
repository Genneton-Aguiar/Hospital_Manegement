# Generated by Django 5.1.1 on 2024-10-18 16:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_remove_payments_user_payments_clinic_value_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.payments')),
            ],
        ),
    ]
