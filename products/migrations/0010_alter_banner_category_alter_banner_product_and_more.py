# Generated by Django 5.0 on 2024-01-03 06:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_sub_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='products.category'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='product',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='products.product'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='sub_category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='products.sub_category'),
        ),
    ]
