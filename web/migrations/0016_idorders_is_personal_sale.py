# Generated by Django 3.1.5 on 2021-03-27 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0015_auto_20210313_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='idorders',
            name='is_personal_sale',
            field=models.BooleanField(default=False, verbose_name='Личная продажа'),
        ),
    ]
