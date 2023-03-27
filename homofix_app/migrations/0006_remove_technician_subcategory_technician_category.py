# Generated by Django 4.1.7 on 2023-03-23 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homofix_app', '0005_remove_technician_category_technician_subcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='technician',
            name='subcategory',
        ),
        migrations.AddField(
            model_name='technician',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='homofix_app.category'),
            preserve_default=False,
        ),
    ]
