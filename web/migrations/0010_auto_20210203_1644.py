# Generated by Django 3.1.5 on 2021-02-03 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_auto_20210203_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='PotrebCredits',
            fields=[
                ('credits_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='web.credits')),
            ],
            options={
                'verbose_name': 'Потребительский кредит',
                'verbose_name_plural': 'Потребительские кредиты',
                'ordering': ('bank_name', 'type'),
            },
            bases=('web.credits',),
        ),
        migrations.AlterModelOptions(
            name='credits',
            options={'ordering': ('bank_name', 'type'), 'verbose_name': 'Кредит', 'verbose_name_plural': 'Кредиты'},
        ),
    ]
