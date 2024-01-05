# Generated by Django 5.0 on 2024-01-05 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_category_imgg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='imgg',
            field=models.FileField(upload_to='brand'),
        ),
        migrations.AlterField(
            model_name='category',
            name='imgg',
            field=models.FileField(upload_to='category'),
        ),
        migrations.AlterField(
            model_name='p_images',
            name='img',
            field=models.FileField(default=1, upload_to='product_images'),
            preserve_default=False,
        ),
    ]
