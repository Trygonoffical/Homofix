# Generated by Django 4.2 on 2023-05-30 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0056_alter_applicantcarrer_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicantcarrer',
            name='email',
            field=models.EmailField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jobenquiry',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
    ]
