# Generated by Django 4.2 on 2023-05-26 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0047_alter_bookingproduct_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingproduct',
            name='booking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homofix_app.booking'),
        ),
    ]
