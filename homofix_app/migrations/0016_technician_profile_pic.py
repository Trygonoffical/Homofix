# Generated by Django 4.1.6 on 2023-02-14 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0015_alter_technician_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='technician',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='Technician'),
        ),
    ]
