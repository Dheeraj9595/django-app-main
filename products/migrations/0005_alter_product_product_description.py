# Generated by Django 4.1.5 on 2023-05-10 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_salesdata_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_description',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]