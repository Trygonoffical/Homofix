# Generated by Django 4.1.7 on 2023-03-16 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0002_remove_product_category_product_subcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingproduct',
            name='total_price',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
