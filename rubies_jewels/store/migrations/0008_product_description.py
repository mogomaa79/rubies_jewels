# Generated by Django 5.0.4 on 2024-05-31 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_productimage_remove_product_image_product_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(default=1, max_length=500),
            preserve_default=False,
        ),
    ]
