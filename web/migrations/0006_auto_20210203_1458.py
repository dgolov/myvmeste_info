# Generated by Django 3.1.5 on 2021-02-03 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20210203_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активен'),
        ),
    ]
