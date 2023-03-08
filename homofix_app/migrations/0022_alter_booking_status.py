# Generated by Django 4.1.7 on 2023-03-05 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0021_alter_support_status_alter_technician_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('in_process', 'In Process'), ('cancelled', 'Cancelled'), ('completed', 'Completed'), ('Assign', 'Assign')], default='New', max_length=20),
        ),
    ]
