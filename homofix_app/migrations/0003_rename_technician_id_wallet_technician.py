# Generated by Django 4.2 on 2023-04-11 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0002_rename_technician_wallet_technician_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wallet',
            old_name='technician_id',
            new_name='technician',
        ),
    ]
