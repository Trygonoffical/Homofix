# Generated by Django 4.1.7 on 2023-02-28 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0002_remove_technician_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='technician',
            name='user_id',
            field=models.CharField(blank=True, max_length=12),
        ),
    ]