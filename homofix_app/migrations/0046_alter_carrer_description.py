# Generated by Django 4.2 on 2023-05-24 12:29

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0045_alter_carrer_status_applicantcarrer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrer',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
