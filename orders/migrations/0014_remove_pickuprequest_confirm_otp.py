# Generated by Django 4.2.1 on 2023-07-28 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_usertransactiondetails_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pickuprequest',
            name='confirm_otp',
        ),
    ]
