# Generated by Django 4.2.1 on 2023-07-27 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_usermodel_upiid'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='pickup_otp',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
