# Generated by Django 4.2.6 on 2023-11-06 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_product_category_product_production_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='manufacturer',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='media/'),
        ),
    ]
