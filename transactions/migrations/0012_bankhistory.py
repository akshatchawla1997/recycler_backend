# Generated by Django 4.2.1 on 2023-08-14 06:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0011_wallethistory_order_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankHistory',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('refrence_id', models.IntegerField()),
                ('status', models.CharField(choices=[('success', 'Success'), ('failed', 'failed')], default='null', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
