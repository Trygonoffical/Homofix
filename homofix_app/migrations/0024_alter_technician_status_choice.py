# Generated by Django 4.1.7 on 2023-03-05 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0023_technician_status_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technician',
            name='status_choice',
            field=models.CharField(choices=[('New', 'New'), ('Accept', 'Accept'), ('Reject', 'Reject'), ('Assign', 'Assign'), ('in_process', 'In Process'), ('Reached', 'Reached'), ('completed', 'Completed')], default='New', max_length=50),
        ),
    ]
