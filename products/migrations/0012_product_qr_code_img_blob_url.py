# Generated by Django 4.1.5 on 2023-05-30 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_alter_qrcodecutomizationtemplates_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='qr_code_img_blob_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
