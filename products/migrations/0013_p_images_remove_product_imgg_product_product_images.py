# Generated by Django 5.0 on 2024-01-04 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_alter_product_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='P_Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.FileField(blank=True, null=True, upload_to='product_images')),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='imgg',
        ),
        migrations.AddField(
            model_name='product',
            name='product_images',
            field=models.ManyToManyField(blank=True, null=True, to='products.p_images'),
        ),
    ]