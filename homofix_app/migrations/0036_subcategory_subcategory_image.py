# Generated by Django 4.2 on 2023-05-18 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0035_category_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='subcategory_image',
            field=models.ImageField(blank=True, null=True, upload_to='subcategory-Image'),
        ),
    ]
