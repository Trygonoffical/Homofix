# Generated by Django 4.2 on 2023-05-16 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0031_alter_mostviewed_img'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mostviewed',
            old_name='proudct',
            new_name='product_id',
        ),
    ]
