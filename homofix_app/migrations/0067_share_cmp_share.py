# Generated by Django 4.2 on 2023-06-11 15:18

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0066_alter_payment_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='share',
            name='cmp_share',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
    ]
