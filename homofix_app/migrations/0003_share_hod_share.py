# Generated by Django 4.1.7 on 2023-03-28 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0002_alter_share_technician_share'),
    ]

    operations = [
        migrations.AddField(
            model_name='share',
            name='hod_share',
            field=models.IntegerField(default=0),
        ),
    ]