# Generated by Django 4.2 on 2023-04-17 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0016_attendance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='user',
            new_name='support_id',
        ),
    ]
