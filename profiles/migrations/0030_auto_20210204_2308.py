# Generated by Django 3.1.5 on 2021-02-04 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0029_auto_20210204_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referralcodes',
            name='qr_code',
            field=models.ImageField(blank=True, upload_to='qr_code'),
        ),
    ]
