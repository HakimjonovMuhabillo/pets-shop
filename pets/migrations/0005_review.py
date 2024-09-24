# Generated by Django 5.1 on 2024-09-05 07:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0004_product_in_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('review', models.TextField()),
                ('rating', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='reviews')),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='pets.product')),
            ],
        ),
    ]