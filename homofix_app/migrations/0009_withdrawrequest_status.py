# Generated by Django 4.2 on 2023-04-12 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0008_product_selling_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawrequest',
            name='status',
            field=models.CharField(choices=[('Process', 'Process'), ('Completed', 'Completed')], default='Process', max_length=50),
        ),
    ]