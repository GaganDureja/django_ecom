# Generated by Django 5.0 on 2023-12-29 06:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=555)),
                ('sort_no', models.IntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='products.category')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='products.product')),
                ('sub_category', models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='products.sub_category')),
            ],
        ),
    ]
