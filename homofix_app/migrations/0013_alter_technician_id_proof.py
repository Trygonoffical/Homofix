# Generated by Django 4.1.6 on 2023-02-14 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0012_alter_technician_id_proof'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technician',
            name='Id_Proof',
            field=models.CharField(blank=True, choices=[('FP', 'Feature Product'), ('LP', 'Latest Product'), ('TP', 'Trending Products'), ('TRP', 'Top Rated Products')], max_length=100, null=True),
        ),
    ]
