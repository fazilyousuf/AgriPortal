# Generated by Django 4.2.6 on 2023-11-06 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_rename_addproduct_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='production_date',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
