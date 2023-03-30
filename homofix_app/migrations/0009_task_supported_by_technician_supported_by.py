# Generated by Django 4.1.7 on 2023-03-29 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0008_share_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='supported_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='homofix_app.support'),
        ),
        migrations.AddField(
            model_name='technician',
            name='supported_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='homofix_app.support'),
        ),
    ]