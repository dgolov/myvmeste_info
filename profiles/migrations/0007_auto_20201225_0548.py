# Generated by Django 3.1.4 on 2020-12-25 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20201224_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='money',
            name='available',
            field=models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Средства на балансе'),
        ),
        migrations.AlterField(
            model_name='money',
            name='paid_out',
            field=models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Выплачено'),
        ),
        migrations.AlterField(
            model_name='money',
            name='reserved',
            field=models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Зарезервировано к выплате'),
        ),
        migrations.AlterField(
            model_name='money',
            name='under_consideration',
            field=models.DecimalField(decimal_places=2, max_digits=7, verbose_name='На рассмотрении'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='balance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balance', to='profiles.money', verbose_name='Баланс'),
        ),
    ]
