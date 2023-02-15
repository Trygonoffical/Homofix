# Generated by Django 4.1.6 on 2023-02-15 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0017_remove_technician_id_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='technician',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Deactivate', 'Deactivate'), ('Hold', 'Hold')], default='Active', max_length=50),
        ),
    ]
