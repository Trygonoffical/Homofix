# Generated by Django 4.2 on 2023-05-26 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0053_jobenquiry_expert_in'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobenquiry',
            name='full_address',
            field=models.TextField(default=2),
            preserve_default=False,
        ),
    ]
