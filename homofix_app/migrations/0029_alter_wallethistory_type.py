# Generated by Django 4.2 on 2023-05-10 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0028_alter_wallethistory_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallethistory',
            name='type',
            field=models.CharField(choices=[('bonus', 'Bonus'), ('deduction', 'Deduction')], max_length=10),
        ),
    ]
