# Generated by Django 4.1.7 on 2023-03-09 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rebooking',
            name='task',
        ),
        migrations.AddField(
            model_name='rebooking',
            name='booking',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='rebookings', to='homofix_app.booking'),
            preserve_default=False,
        ),
    ]
