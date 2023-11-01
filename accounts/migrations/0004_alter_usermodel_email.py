# Generated by Django 4.2.1 on 2023-08-23 11:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_usermodel_pickup_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='email',
            field=models.EmailField(blank=True, max_length=50, null=True, unique=True, validators=[django.core.validators.EmailValidator()]),
        ),
    ]
