# Generated by Django 5.1 on 2024-08-19 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0002_color_color_product_sku_product_slug_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sales',
            field=models.IntegerField(default=0),
        ),
    ]
