# Generated by Django 4.1.6 on 2023-02-14 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0010_alter_technician_id_proof'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technician',
            name='Id_Proof',
            field=models.CharField(blank=True, choices=[('Adhaar', 'Adhaar Card'), ('voter_id', 'Voter Id'), ('Driving Lisence', 'Driving Lisence')], max_length=100, null=True),
        ),
    ]
