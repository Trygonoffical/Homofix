# Generated by Django 4.1.6 on 2023-02-14 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0014_alter_technician_id_proof'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technician',
            name='mobile',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
