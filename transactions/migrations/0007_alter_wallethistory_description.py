# Generated by Django 4.2.1 on 2023-08-03 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_wallethistory_wallet_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallethistory',
            name='description',
            field=models.CharField(choices=[('redeemed', 'Redeemed'), ('amount_added', 'Amount_Added')], default='null', max_length=100),
        ),
    ]
