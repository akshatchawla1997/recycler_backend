# Generated by Django 4.2.1 on 2023-07-13 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_alter_orders_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_status',
            field=models.CharField(choices=[('live', 'Live'), ('on hold', 'On Hold'), ('completed', 'Completed'), ('rejected', 'Rejected')], default='on hold', max_length=100),
        ),
    ]